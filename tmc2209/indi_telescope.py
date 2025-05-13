#!/usr/bin/env python3
"""
INDI driver implementation for TMC2209-controlled telescope
This script creates a custom INDI driver for telescope control with KStars/Ekos
"""
import os
import sys
import time
import math
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TelescopeDriver')

# Try to import PyIndi - if not available, guide the user to install it
try:
    import PyIndi
except ImportError:
    logger.error("PyIndi module not found. Install with: pip install pyindi-client")
    logger.error("If that fails, install from source: https://github.com/indilib/pyindi-client")
    sys.exit(1)

# Try to import RPi.GPIO for motor control
try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.error("RPi.GPIO module not found. Install with: pip install RPi.GPIO")
    sys.exit(1)

class IndiTelescopeDriver(PyIndi.BaseClient):
    """INDI client implementation for a TMC2209-controlled telescope"""
    
    def __init__(self):
        super(IndiTelescopeDriver, self).__init__()
        
        # Configure motor control pins
        self.STEP_PIN_RA = 21    # RA (Right Ascension) motor
        self.DIR_PIN_RA = 20
        self.ENABLE_PIN_RA = 16
        
        self.STEP_PIN_DEC = 19   # DEC (Declination) motor
        self.DIR_PIN_DEC = 26
        self.ENABLE_PIN_DEC = 13
        
        # Motor parameters
        self.STEPS_PER_REV = 200          # For a 1.8° stepper
        self.MICROSTEPS = 16              # Microstepping factor
        self.GEAR_RATIO = 100             # Gear reduction ratio
        self.STEPS_PER_DEG = (self.STEPS_PER_REV * self.MICROSTEPS * self.GEAR_RATIO) / 360
        
        # Motor state tracking
        self.ra_position = 0    # in degrees
        self.dec_position = 0   # in degrees
        self.is_tracking = False
        self.tracking_thread = None
        self.stop_tracking = threading.Event()
        
        # Initialize GPIO
        self._setup_gpio()
        
        logger.info("TMC2209 Telescope Driver initialized")
    
    def _setup_gpio(self):
        """Setup GPIO pins for motor control"""
        GPIO.setmode(GPIO.BCM)
        
        # Setup RA motor pins
        GPIO.setup(self.STEP_PIN_RA, GPIO.OUT)
        GPIO.setup(self.DIR_PIN_RA, GPIO.OUT)
        GPIO.setup(self.ENABLE_PIN_RA, GPIO.OUT)
        
        # Setup DEC motor pins
        GPIO.setup(self.STEP_PIN_DEC, GPIO.OUT)
        GPIO.setup(self.DIR_PIN_DEC, GPIO.OUT)
        GPIO.setup(self.ENABLE_PIN_DEC, GPIO.OUT)
        
        # Initially disable motors
        GPIO.output(self.ENABLE_PIN_RA, GPIO.HIGH)
        GPIO.output(self.ENABLE_PIN_DEC, GPIO.HIGH)
    
    def connect_server(self):
        """Connect to the INDI server"""
        self.setServer("localhost", 7624)
        if not self.connectServer():
            logger.error("Failed to connect to INDI server")
            return False
        logger.info("Connected to INDI server")
        return True
    
    def newDevice(self, deviceName):
        """Callback when a new device is detected - override from BaseClient"""
        logger.info(f"New device: {deviceName}")
    
    def newProperty(self, property):
        """Callback when a new property is detected - override from BaseClient"""
        device = property.getDeviceName()
        name = property.getName()
        logger.debug(f"New property: {device}.{name}")
    
    def move_ra(self, degrees, direction=1):
        """Move Right Ascension motor by specified degrees"""
        steps = int(abs(degrees) * self.STEPS_PER_DEG)
        
        # Enable motor
        GPIO.output(self.ENABLE_PIN_RA, GPIO.LOW)
        
        # Set direction
        GPIO.output(self.DIR_PIN_RA, GPIO.HIGH if direction > 0 else GPIO.LOW)
        
        # Calculate step delay for sidereal tracking (if needed)
        # This is simplified - real implementation would be more precise
        step_delay = 0.0002  # Default fast slew
        
        logger.info(f"Moving RA motor {degrees} degrees ({steps} steps)")
        
        # Perform steps
        for _ in range(steps):
            GPIO.output(self.STEP_PIN_RA, GPIO.HIGH)
            time.sleep(step_delay)
            GPIO.output(self.STEP_PIN_RA, GPIO.LOW)
            time.sleep(step_delay)
        
        # Update position
        self.ra_position += degrees * direction
        
        # Disable motor if not tracking
        if not self.is_tracking:
            GPIO.output(self.ENABLE_PIN_RA, GPIO.HIGH)
    
    def move_dec(self, degrees, direction=1):
        """Move Declination motor by specified degrees"""
        steps = int(abs(degrees) * self.STEPS_PER_DEG)
        
        # Enable motor
        GPIO.output(self.ENABLE_PIN_DEC, GPIO.LOW)
        
        # Set direction
        GPIO.output(self.DIR_PIN_DEC, GPIO.HIGH if direction > 0 else GPIO.LOW)
        
        logger.info(f"Moving DEC motor {degrees} degrees ({steps} steps)")
        
        # Perform steps
        for _ in range(steps):
            GPIO.output(self.STEP_PIN_DEC, GPIO.HIGH)
            time.sleep(0.0002)
            GPIO.output(self.STEP_PIN_DEC, GPIO.LOW)
            time.sleep(0.0002)
        
        # Update position
        self.dec_position += degrees * direction
        
        # Disable motor
        GPIO.output(self.ENABLE_PIN_DEC, GPIO.HIGH)
    
    def start_tracking(self):
        """Start sidereal tracking in RA axis"""
        if self.is_tracking:
            return
        
        self.is_tracking = True
        self.stop_tracking.clear()
        
        # Enable RA motor for tracking
        GPIO.output(self.ENABLE_PIN_RA, GPIO.LOW)
        
        # Start tracking in a separate thread
        self.tracking_thread = threading.Thread(target=self._tracking_worker)
        self.tracking_thread.daemon = True
        self.tracking_thread.start()
        
        logger.info("Sidereal tracking started")
    
    def stop_tracking(self):
        """Stop sidereal tracking"""
        if not self.is_tracking:
            return
        
        self.stop_tracking.set()
        if self.tracking_thread:
            self.tracking_thread.join()
        
        # Disable RA motor
        GPIO.output(self.ENABLE_PIN_RA, GPIO.HIGH)
        
        self.is_tracking = False
        logger.info("Sidereal tracking stopped")
    
    def _tracking_worker(self):
        """Worker thread for sidereal tracking"""
        # Earth rotates 360 degrees in ~86164 seconds (sidereal day)
        # Calculate delay between steps based on our gearing
        
        sidereal_rate_deg_per_sec = 360.0 / 86164.0
        steps_per_sec = sidereal_rate_deg_per_sec * self.STEPS_PER_DEG
        step_delay = 0.5 / steps_per_sec  # Half period
        
        logger.info(f"Tracking at sidereal rate with step delay {step_delay:.6f}s")
        
        # Set RA direction for tracking (depends on hemisphere and mount type)
        GPIO.output(self.DIR_PIN_RA, GPIO.HIGH)  # Adjust as needed
        
        while not self.stop_tracking.is_set():
            GPIO.output(self.STEP_PIN_RA, GPIO.HIGH)
            time.sleep(step_delay)
            GPIO.output(self.STEP_PIN_RA, GPIO.LOW)
            time.sleep(step_delay)
    
    def cleanup(self):
        """Clean up resources"""
        # Stop tracking if active
        if self.is_tracking:
            self.stop_tracking()
        
        # Disable motors
        GPIO.output(self.ENABLE_PIN_RA, GPIO.HIGH)
        GPIO.output(self.ENABLE_PIN_DEC, GPIO.HIGH)
        
        # Clean up GPIO
        GPIO.cleanup()
        logger.info("Driver resources cleaned up")


def main():
    """Main function to run the INDI telescope driver"""
    driver = IndiTelescopeDriver()
    
    try:
        # Connect to INDI server
        if not driver.connect_server():
            sys.exit(1)
        
        logger.info("Telescope driver running. Press Ctrl+C to exit.")
        
        # Test motor movement
        driver.move_ra(10, 1)    # Move 10 degrees east
        driver.move_dec(5, 1)    # Move 5 degrees north
        
        # Start tracking
        driver.start_tracking()
        
        # Keep the program running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    finally:
        driver.cleanup()
        logger.info("Program exited")


if __name__ == "__main__":
    main()