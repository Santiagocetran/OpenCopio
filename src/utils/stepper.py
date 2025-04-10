"""
Core stepper motor control functions for telescope automation.
Implements basic motor control and movement patterns.
"""

import RPi.GPIO as GPIO
import time
from typing import Dict, Optional

class StepperMotor:
    def __init__(self, pin_config: Dict[str, int], motor_specs: Dict[str, int]):
        """
        Initialize stepper motor with pin configuration and specifications.
        
        Args:
            pin_config: Dictionary containing IN1, IN2, IN3, IN4, and ENABLE pin numbers
            motor_specs: Dictionary containing motor specifications
        """
        self.pins = pin_config
        self.specs = motor_specs
        self.current_position = 0
        self.setup_gpio()
        
    def setup_gpio(self):
        """Configure GPIO pins for motor control."""
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            
    def step(self, direction: int, steps: int, rpm: Optional[int] = None):
        """
        Move motor a specified number of steps in given direction.
        
        Args:
            direction: 1 for clockwise, -1 for counterclockwise
            steps: Number of steps to move
            rpm: Optional RPM value (defaults to DEFAULT_RPM from specs)
        """
        if rpm is None:
            rpm = self.specs['DEFAULT_RPM']
            
        step_delay = 60.0 / (rpm * self.specs['STEPS_PER_REVOLUTION'])
        
        for _ in range(steps):
            self._single_step(direction)
            time.sleep(step_delay)
            self.current_position += direction
            
    def _single_step(self, direction: int):
        """Execute a single step in the specified direction."""
        # Implementation will be added in the next phase
        pass
        
    def set_speed(self, rpm: int):
        """Set motor speed in RPM."""
        if rpm < self.specs['MIN_RPM'] or rpm > self.specs['MAX_RPM']:
            raise ValueError(f"RPM must be between {self.specs['MIN_RPM']} and {self.specs['MAX_RPM']}")
        self.specs['DEFAULT_RPM'] = rpm
        
    def get_position(self) -> int:
        """Return current motor position in steps."""
        return self.current_position
        
    def cleanup(self):
        """Clean up GPIO resources."""
        for pin in self.pins.values():
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup() 