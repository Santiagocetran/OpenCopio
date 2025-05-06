# Step-by-Step Guide to Make Your Motors Spin with PyTrinamic

Assuming your TMC2209-V3 drivers and NEMA 17 motors are correctly connected to your Raspberry Pi, here's how to get them spinning using the official PyTrinamic library:

## Step 1: Install Required Libraries
Open a terminal on your Raspberry Pi and run:

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
sudo pip3 install PyTrinamic pyserial
```

## Step 2: Configure UART on Raspberry Pi
Enable UART and disable serial console:

```bash
sudo raspi-config
```

Navigate to:
- Interface Options → Serial
- Disable serial login shell
- Enable serial hardware

After changing settings, reboot:
```bash
sudo reboot
```

## Step 3: Connect TMC2209 UART
Connect your TMC2209 to the Raspberry Pi:
- PDN_UART pin to RPi RX (GPIO15)
- PDN_UART pin to RPi TX (GPIO14) with a 1kΩ resistor in between
- Connect DIR, STEP, and EN pins as usual

## Step 4: Create a Test Script
Create a new Python file:

```bash
nano pytrinamic_test.py
```

## Step 5: Copy This Basic Script
Copy this code into the editor:

```python
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
```

## Step 6: Save and Exit Nano
Press `Ctrl+O` then Enter to save, and `Ctrl+X` to exit.

## Step 7: Run the Script
```bash
sudo python3 pytrinamic_test.py
```

## Step 8: Advanced Features (Optional)
For telescope operation, you may want to add these advanced features to your script:

```python
# Silent StealthChop mode for quiet operation
tmc2209.set_spreadcycle(False)
tmc2209.set_stealthchop_threshold(1000000)  # Always use StealthChop

# Enable CoolStep for dynamic current adjustment
tmc2209.set_coolstep_threshold(1000)

# Configure stallGuard for sensorless homing
tmc2209.set_stallguard_threshold(5)  # Adjust sensitivity as needed
```

## Troubleshooting
If the motor doesn't turn:

1. **Check UART Connection**: Verify your serial connection with:
   ```python
   print(tmc2209.get_info())
   ```

2. **UART Device Issues**: If you get connection errors, try different device paths:
   ```python
   my_interface = connection_manager.connect_serial("/dev/ttyAMA0", 115200)
   ```

3. **Driver Configuration**: If the motor doesn't respond to commands, check registers:
   ```python
   print(tmc2209.get_registers())
   ```

4. **Check Wiring**: Ensure motor wires (A1, A2, B1, B2) are correctly connected to the driver.

5. **Microstepping Issue**: If steps seem incorrect, verify your microstep setting:
   ```python
   actual_microstep = tmc2209.get_microstep_resolution()
   print(f"Current microstepping: 1/{actual_microstep}")
   ```

## Adjusting Parameters for Telescopes
For telescope control:

* **Tracking Speed**: For sidereal tracking (Earth rotation), use very slow speeds:
  ```python
  # Assuming 200 steps/revolution, 1:100 gear ratio, 1/16 microstepping
  # Sidereal rate ~= 15 arcsec/second
  step_delay = 0.0082  # Calculate this based on your gear ratio
  ```

* **Microstepping**: Use higher values (1/16 or 1/32) for smooth tracking:
  ```python
  tmc2209.set_microstep_resolution(32)  # 1/32 microstepping for smoother motion
  ```

* **Current Control**: Use just enough current for smooth motion without heat:
  ```python
  # Use lower current for tracking, higher for slewing
  tmc2209.set_motor_run_current(400)  # 400mA during tracking
  ```
