#!/usr/bin/env python3
"""
Advanced TMC2209 stepper motor control using PyTrinamic library
This script configures driver settings via UART and demonstrates microstepping
"""
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules.tmc2209 import TMC2209
import RPi.GPIO as GPIO
import time

# Define standard GPIO pins (adjust to match your wiring)
STEP_PIN = 21    # GPIO pin connected to STEP on TMC2209
DIR_PIN = 20     # GPIO pin connected to DIR on TMC2209
ENABLE_PIN = 16  # GPIO pin connected to ENN on TMC2209

# Setup GPIO for step/dir control
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

# Initialize serial connection to TMC2209 (UART mode)
# Typical Raspberry Pi UART is at /dev/ttyS0 or /dev/ttyAMA0
connection_manager = ConnectionManager()
my_interface = connection_manager.connect_serial("/dev/ttyS0", 115200)

# Create a TMC2209 module instance (address 0)
tmc2209 = TMC2209(my_interface, 0)

print("TMC2209 info:")
print("Driver type: " + tmc2209.get_name())
print("Driver version: " + tmc2209.get_version())

# Configure driver settings via UART
# StealthChop (quiet) mode
tmc2209.set_spreadcycle(False) 
# Motor current in mA (adjust for your motor, typically 500-1200mA for NEMA 17)
tmc2209.set_motor_run_current(800)
# Microstepping to 1/16 (options: 1, 2, 4, 8, 16, 32, 64, 128, 256)
tmc2209.set_microstep_resolution(16)

# Enable the driver (LOW enables the TMC2209)
GPIO.output(ENABLE_PIN, GPIO.LOW)

try:
    # Set direction (HIGH = clockwise, LOW = counterclockwise)
    print("Moving clockwise...")
    GPIO.output(DIR_PIN, GPIO.HIGH)
    
    # Move 3200 steps (one full rotation at 1/16 microstepping for 1.8° stepper)
    for i in range(3200):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(0.0002)  # Faster speed due to microstepping
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(0.0002)
    
    time.sleep(1)  # Pause for a second
    
    # Change direction
    print("Moving counterclockwise...")
    GPIO.output(DIR_PIN, GPIO.LOW)
    
    # Move 3200 steps in the other direction
    for i in range(3200):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(0.0002)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(0.0002)
        
except KeyboardInterrupt:
    # Exit on Ctrl+C
    print("Motor stopped")
    
finally:
    # Disable the driver and cleanup GPIO
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # HIGH disables the driver
    GPIO.cleanup()
    my_interface.close()
    print("GPIO cleaned up and connection closed")