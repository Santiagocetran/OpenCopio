# Step-by-Step Guide to Make Your Motors Spin

Assuming your TMC2209-V3 drivers and NEMA 17 motors are correctly connected to your Raspberry Pi, here's how to get them spinning:

## Step 1: Install Required Libraries
Open a terminal on your Raspberry Pi and run:

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
sudo pip3 install RPi.GPIO
```

## Step 2: Create a Test Script
Create a new Python file:

```bash
nano stepper_test.py
```

## Step 3: Copy This Basic Script
Copy this code into the editor:

```python
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
```

## Step 4: Save and Exit Nano
Press `Ctrl+O` then Enter to save, and `Ctrl+X` to exit.

## Step 5: Run the Script

```bash
sudo python3 stepper_test.py
```

## Step 6: Troubleshooting
If the motor doesn't turn:

1. **Check Enable Pin**: Some TMC2209 modules need the enable pin HIGH instead of LOW. Try changing:

```python
GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Try this if LOW doesn't work
```

2. **Check Wiring**: Ensure your motor wires (A1, A2, B1, B2) are correctly connected to the driver.

3. **Adjust Speed**: The delay values (0.005) might be too fast or slow for your setup. Try increasing this value to 0.01 or higher if the motor stalls.

4. **Check Power**: Ensure your power supply can deliver enough current (typically 1-2A for NEMA 17 motors).

## Step 7: Adjusting Parameters
To modify the motor behavior:

* Change the number in `range(200)` to adjust how many steps the motor takes
* Modify the `time.sleep()` values to change speed
* If you're using microstepping, you'll need more steps for a full rotation
