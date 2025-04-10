#!/usr/bin/env python3
"""
Quick test script for NEMA17 stepper motor with L298N
Runs a predefined test sequence automatically
"""
import RPi.GPIO as GPIO
import time

# Motor pins - adjust to match your wiring
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set pins as outputs
pins = [IN1, IN2, IN3, IN4]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Step sequence for half-stepping (8 steps)
sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

try:
    print("Running test sequence...")
    
    # Test 1: 360° clockwise rotation (200 steps for NEMA17)
    print("Testing: 360° clockwise")
    for _ in range(200):  # Adjust if your motor has different steps/revolution
        for step in range(8):
            for i in range(4):
                GPIO.output(pins[i], sequence[step][i])
            time.sleep(0.003)  # Speed control
    
    time.sleep(1)  # Pause between tests
    
    # Test 2: 360° counterclockwise
    print("Testing: 360° counterclockwise")
    for _ in range(200):
        for step in range(7, -1, -1):
            for i in range(4):
                GPIO.output(pins[i], sequence[step][i])
            time.sleep(0.003)
    
    print("Test complete!")

except KeyboardInterrupt:
    print("Test interrupted")

finally:
    # Turn off motor
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()