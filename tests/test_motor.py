"""
Basic motor control tests for telescope automation system.
"""

import pytest
from src.config import MOTOR_X, MOTOR_Y, MOTOR_SPECS, CALIBRATION
from src.utils.stepper import StepperMotor
from src.utils.calibration import Calibration

def test_motor_initialization():
    """Test motor initialization and GPIO setup."""
    motor = StepperMotor(MOTOR_X, MOTOR_SPECS)
    assert motor is not None
    motor.cleanup()

def test_basic_movement():
    """Test basic motor movement."""
    motor = StepperMotor(MOTOR_X, MOTOR_SPECS)
    
    # Test forward movement
    initial_pos = motor.get_position()
    motor.step(1, 100)  # Move 100 steps forward
    assert motor.get_position() == initial_pos + 100
    
    # Test backward movement
    motor.step(-1, 50)  # Move 50 steps backward
    assert motor.get_position() == initial_pos + 50
    
    motor.cleanup()

def test_speed_control():
    """Test motor speed control."""
    motor = StepperMotor(MOTOR_X, MOTOR_SPECS)
    
    # Test valid speed setting
    motor.set_speed(30)
    assert motor.specs['DEFAULT_RPM'] == 30
    
    # Test invalid speed setting
    with pytest.raises(ValueError):
        motor.set_speed(100)  # Above MAX_RPM
    
    motor.cleanup()

def test_calibration():
    """Test basic calibration procedures."""
    motor = StepperMotor(MOTOR_X, MOTOR_SPECS)
    cal = Calibration(motor, CALIBRATION)
    
    # Test position limits
    cal.set_limits(-1000, 1000)
    min_limit, max_limit = cal.get_position_limits()
    assert min_limit == -1000
    assert max_limit == 1000
    
    motor.cleanup()

if __name__ == "__main__":
    pytest.main([__file__]) 