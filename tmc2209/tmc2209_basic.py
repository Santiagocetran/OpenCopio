#!/usr/bin/env python3
"""
Basic TMC2209 stepper motor test script for Raspberry Pi
Simple step/direction control without advanced features
"""
import RPi.GPIO as GPIO
import time

# Define your GPIO pins (adjust these to match your wiring)
STEP_PIN = 21    # GPIO pin connected to STEP on TMC2209
DIR_PIN = 20     # GPIO pin connected to DIR on TMC2209
ENABLE_PIN = 16  # GPIO pin connected to ENN on TMC2209

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

# Enable the driver (LOW enables the TMC2209)
GPIO.output(ENABLE_PIN, GPIO.LOW)

try:
    # Set direction (HIGH = clockwise, LOW = counterclockwise)
    print("Moving clockwise...")
    GPIO.output(DIR_PIN, GPIO.HIGH)
    
    # Move 200 steps (one full rotation for 1.8° stepper)
    for i in range(200):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(0.005)  # Adjust this delay to change speed
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(0.005)  # Adjust this delay to change speed
    
    time.sleep(1)  # Pause for a second
    
    # Change direction
    print("Moving counterclockwise...")
    GPIO.output(DIR_PIN, GPIO.LOW)
    
    # Move 200 steps in the other direction
    for i in range(200):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(0.005)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(0.005)
        
except KeyboardInterrupt:
    # Exit on Ctrl+C
    print("Motor stopped")
    
finally:
    # Disable the driver and cleanup GPIO
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # HIGH disables the driver
    GPIO.cleanup()
    print("GPIO cleaned up")