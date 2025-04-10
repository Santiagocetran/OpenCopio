"""
Configuration settings for telescope control system.
Contains pin assignments and motor specifications.
"""

# GPIO Pin Assignments
MOTOR_X = {
    'IN1': 17,  # GPIO pin for X motor IN1
    'IN2': 18,  # GPIO pin for X motor IN2
    'IN3': 22,  # GPIO pin for X motor IN3
    'IN4': 23,  # GPIO pin for X motor IN4
    'ENABLE': 24  # GPIO pin for X motor enable
}

MOTOR_Y = {
    'IN1': 5,   # GPIO pin for Y motor IN1
    'IN2': 6,   # GPIO pin for Y motor IN2
    'IN3': 13,  # GPIO pin for Y motor IN3
    'IN4': 19,  # GPIO pin for Y motor IN4
    'ENABLE': 26  # GPIO pin for Y motor enable
}

# Motor Specifications
MOTOR_SPECS = {
    'STEPS_PER_REVOLUTION': 200,  # NEMA17 standard steps per revolution
    'MAX_RPM': 60,  # Maximum safe RPM
    'MIN_RPM': 1,   # Minimum practical RPM
    'DEFAULT_RPM': 30  # Default operating RPM
}

# Calibration Settings
CALIBRATION = {
    'STEPS_PER_DEGREE': 200,  # Steps required for 1 degree of movement
    'MAX_STEPS': 10000,  # Maximum steps before limit
    'HOME_POSITION': 0  # Default home position
} 