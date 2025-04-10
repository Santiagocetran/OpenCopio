# Telescope Control System

A Python-based control system for automating telescope movements using NEMA17 stepper motors and L298N motor controllers on Raspberry Pi 4.

## Project Structure

- `src/main.py`: Main control script for motor operations
- `src/config.py`: Configuration settings for pins and motor specifications
- `src/utils/stepper.py`: Core stepper motor control functions
- `src/utils/calibration.py`: Calibration procedures and utilities
- `tests/test_motor.py`: Basic motor control tests

## Hardware Requirements

- Raspberry Pi 4
- NEMA17 Stepper Motors (x2 for X/Y axes)
- L298N Motor Controllers (x2)
- Power supply (12V recommended)
- Jumper wires
- Breadboard (optional)

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Connect hardware:
   - Connect L298N controllers to Raspberry Pi GPIO pins
   - Connect stepper motors to L298N controllers
   - Connect power supply to L298N controllers

3. Update pin configurations in `config.py` to match your setup

4. Run basic tests:
   ```bash
   python tests/test_motor.py
   ```

## Safety Notes

- Always power off the system before making connections
- Ensure proper voltage and current ratings for your motors
- Keep wiring organized and secure
- Monitor motor temperatures during operation

## Future Features

- Focus control integration
- Advanced calibration procedures
- Remote control interface
- Position tracking and limits 