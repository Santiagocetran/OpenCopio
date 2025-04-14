#!/usr/bin/env python3
"""
PWM test script for NEMA17 stepper motor with L298N controller on Raspberry Pi.
Tests power/speed control using PWM while maintaining step sequence.

Note: This is not true microstepping - the L298N isn't designed for that.
This script mainly experiments with power/torque control via PWM.
"""
import RPi.GPIO as GPIO
import time

# Motor pins - using the same pins as in the original scripts
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# PWM frequency (Hz)
PWM_FREQ = 100

# Setup
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Set pins as outputs
    pins = [IN1, IN2, IN3, IN4]
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    # Initialize PWM on all pins
    pwm_pins = [GPIO.PWM(pin, PWM_FREQ) for pin in pins]
    for pwm in pwm_pins:
        pwm.start(0)  # Start with 0% duty cycle
    
    return pwm_pins

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

def move_motor(pwm_pins, steps, direction, duty_cycle=50, step_delay=0.003):
    """
    Move the motor with PWM control
    
    Args:
        pwm_pins: List of PWM objects for each pin
        steps: Number of steps to move
        direction: 1 for clockwise, -1 for counterclockwise
        duty_cycle: PWM duty cycle (0-100) - controls power/torque
        step_delay: Delay between steps - controls speed
    """
    step_counter = 0
    
    for _ in range(steps):
        # Update step counter based on direction
        if direction == 1:  # Clockwise
            step_counter = (step_counter + 1) % 8
        else:  # Counterclockwise
            step_counter = (step_counter - 1) % 8
        
        # Apply the step with PWM
        for i in range(4):
            if sequence[step_counter][i] == 1:
                pwm_pins[i].ChangeDutyCycle(duty_cycle)
            else:
                pwm_pins[i].ChangeDutyCycle(0)
        
        time.sleep(step_delay)
    
    # Turn off all pins after movement
    for pwm in pwm_pins:
        pwm.ChangeDutyCycle(0)

def cleanup(pwm_pins):
    """Clean up GPIO resources."""
    for pwm in pwm_pins:
        pwm.stop()
    GPIO.cleanup()

def pwm_test():
    """Run tests with various PWM settings."""
    try:
        pwm_pins = setup()
        print("PWM Stepper Motor Test")
        print("---------------------")
        
        # Test 1: Standard duty cycle (50%)
        print("\nTest 1: 100 steps clockwise at 50% power")
        move_motor(pwm_pins, 100, 1, duty_cycle=50)
        time.sleep(1)
        
        # Test 2: Lower duty cycle - less power/torque
        print("\nTest 2: 100 steps clockwise at 25% power")
        move_motor(pwm_pins, 100, 1, duty_cycle=25)
        time.sleep(1)
        
        # Test 3: Higher duty cycle - more power/torque
        print("\nTest 3: 100 steps clockwise at 90% power")
        move_motor(pwm_pins, 100, 1, duty_cycle=90)
        time.sleep(1)
        
        # Test 4: Speed variation
        print("\nTest 4: 100 steps counterclockwise at 50% power with slower speed")
        move_motor(pwm_pins, 100, -1, duty_cycle=50, step_delay=0.008)
        time.sleep(1)
        
        # Test 5: Speed variation
        print("\nTest 5: 100 steps counterclockwise at 50% power with faster speed")
        move_motor(pwm_pins, 100, -1, duty_cycle=50, step_delay=0.001)
        
        print("\nTests complete!")
    
    except KeyboardInterrupt:
        print("\nTest interrupted")
    
    finally:
        cleanup(pwm_pins)

def interactive_pwm_test():
    """Interactive PWM testing with user control."""
    try:
        pwm_pins = setup()
        print("Interactive PWM Stepper Motor Control")
        print("------------------------------------")
        print("Commands:")
        print("  c STEPS POWER - Move STEPS steps clockwise at POWER% power (1-100)")
        print("  a STEPS POWER - Move STEPS steps counterclockwise at POWER% power (1-100)")
        print("  s STEPS POWER DELAY - Move with custom delay (in milliseconds)")
        print("  q - Quit the program")
        
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command.startswith('q'):
                break
                
            elif command.startswith('c '):
                try:
                    parts = command.split()
                    steps = int(parts[1])
                    power = int(parts[2])
                    if power < 1 or power > 100:
                        print("Power must be between 1 and 100")
                        continue
                    print(f"Moving {steps} steps clockwise at {power}% power...")
                    move_motor(pwm_pins, steps, 1, duty_cycle=power)
                    print("Done")
                except (ValueError, IndexError):
                    print("Error: Please enter valid numbers.")
                    
            elif command.startswith('a '):
                try:
                    parts = command.split()
                    steps = int(parts[1])
                    power = int(parts[2])
                    if power < 1 or power > 100:
                        print("Power must be between 1 and 100")
                        continue
                    print(f"Moving {steps} steps counterclockwise at {power}% power...")
                    move_motor(pwm_pins, steps, -1, duty_cycle=power)
                    print("Done")
                except (ValueError, IndexError):
                    print("Error: Please enter valid numbers.")
            
            elif command.startswith('s '):
                try:
                    parts = command.split()
                    steps = int(parts[1])
                    power = int(parts[2])
                    delay_ms = float(parts[3])
                    delay_sec = delay_ms / 1000.0
                    if power < 1 or power > 100:
                        print("Power must be between 1 and 100")
                        continue
                    print(f"Moving {steps} steps clockwise at {power}% power with {delay_ms}ms delay...")
                    move_motor(pwm_pins, steps, 1, duty_cycle=power, step_delay=delay_sec)
                    print("Done")
                except (ValueError, IndexError):
                    print("Error: Please enter valid numbers.")
                    
            else:
                print("Unknown command. Try again.")
    
    except KeyboardInterrupt:
        print("\nExiting program")
    
    finally:
        cleanup(pwm_pins)

if __name__ == "__main__":
    # Choose which mode to run
    mode = input("Select mode (1 for automatic test, 2 for interactive): ").strip()
    if mode == "1":
        pwm_test()
    elif mode == "2":
        interactive_pwm_test()
    else:
        print("Invalid selection. Exiting.")