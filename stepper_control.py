#!/usr/bin/env python3
"""
Simple script to control NEMA17 stepper motor with L298N controller on Raspberry Pi 4.
"""
import RPi.GPIO as GPIO
import time
import sys

# Motor pin configuration (BCM numbering)
IN1 = 17  # GPIO pin connected to IN1 on L298N
IN2 = 18  # GPIO pin connected to IN2 on L298N
IN3 = 27  # GPIO pin connected to IN3 on L298N
IN4 = 22  # GPIO pin connected to IN4 on L298N

# Motor settings
STEP_DELAY = 0.003  # Time between steps (seconds) - controls speed

def setup():
    """Set up GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup all pins as outputs
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    
    # Initialize all pins to LOW
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def single_step(step_number):
    """Perform a single step based on step number (0-7)."""
    # 8-step sequence for smoother motion
    if step_number == 0:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
    elif step_number == 1:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
    elif step_number == 2:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
    elif step_number == 3:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif step_number == 4:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif step_number == 5:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.HIGH)
    elif step_number == 6:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    elif step_number == 7:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)

def move_motor(steps, direction):
    """
    Move motor a number of steps in the specified direction.
    
    Args:
        steps: Number of steps to move
        direction: 1 for clockwise, -1 for counterclockwise
    """
    step_counter = 0
    
    # Loop through the required number of steps
    for i in range(steps):
        # Update step counter based on direction
        if direction == 1:  # Clockwise
            step_counter = (step_counter + 1) % 8
        else:  # Counterclockwise
            step_counter = (step_counter - 1) % 8
            
        # Execute the step
        single_step(step_counter)
        time.sleep(STEP_DELAY)
    
    # Turn off coils after movement
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def cleanup():
    """Clean up GPIO resources."""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.cleanup()

def main():
    """Main function to control the stepper motor."""
    try:
        setup()
        print("Stepper Motor Control")
        print("--------------------")
        print("Commands:")
        print("  c NUMBER - Move NUMBER steps clockwise")
        print("  a NUMBER - Move NUMBER steps counterclockwise")
        print("  q        - Quit the program")
        
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command.startswith('q'):
                break
                
            elif command.startswith('c '):
                try:
                    steps = int(command.split()[1])
                    print(f"Moving {steps} steps clockwise...")
                    move_motor(steps, 1)
                    print("Done")
                except (ValueError, IndexError):
                    print("Error: Please enter a valid number of steps.")
                    
            elif command.startswith('a '):
                try:
                    steps = int(command.split()[1])
                    print(f"Moving {steps} steps counterclockwise...")
                    move_motor(steps, -1)
                    print("Done")
                except (ValueError, IndexError):
                    print("Error: Please enter a valid number of steps.")
                    
            else:
                print("Unknown command. Try again.")
                
    except KeyboardInterrupt:
        print("\nExiting program")
    finally:
        cleanup()

if __name__ == "__main__":
    main()