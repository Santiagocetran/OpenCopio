# Telescope Control with TMC2209 Stepper Drivers

This repository contains scripts and documentation for controlling a telescope using TMC2209 stepper motor drivers with a Raspberry Pi, ranging from basic movement to advanced control and software integration.

## Table of Contents

- [Basic TMC2209 Motor Control](#basic-tmc2209-motor-control)
- [Advanced Control with PyTrinamic](#advanced-control-with-pytrinamic)
- [Telescope Integration with INDI](#telescope-integration-with-indi)
- [Hardware Requirements](#hardware-requirements)
- [Wiring Diagrams](#wiring-diagrams)
- [Troubleshooting](#troubleshooting)

## Basic TMC2209 Motor Control

### Step-by-Step Guide to Make Your Motors Spin

Assuming your TMC2209-V3 drivers and NEMA 17 motors are correctly connected to your Raspberry Pi, here's how to get them spinning:

#### Step 1: Install Required Libraries
Open a terminal on your Raspberry Pi and run:

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
sudo pip3 install RPi.GPIO
```

#### Step 2: Run the Test Script
Save the `tmc2209_basic.py` script to your Raspberry Pi, then run:

```bash
sudo python3 tmc2209_basic.py
```

This script will:
1. Configure the GPIO pins for your TMC2209 driver
2. Rotate the motor 200 steps clockwise (one full rotation for a 1.8° stepper)
3. Wait one second
4. Rotate the motor 200 steps counterclockwise

#### Troubleshooting Basic Movement
If the motor doesn't turn:

1. **Check Enable Pin**: Some TMC2209 modules need the enable pin HIGH instead of LOW. Try changing:
   ```python
   GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Try this if LOW doesn't work
   ```

2. **Check Wiring**: Ensure your motor wires (A1, A2, B1, B2) are correctly connected to the driver.

3. **Adjust Speed**: The delay values (0.005) might be too fast or slow for your setup. Try increasing this value to 0.01 or higher if the motor stalls.

4. **Check Power**: Ensure your power supply can deliver enough current (typically 1-2A for NEMA 17 motors).

## Advanced Control with PyTrinamic

### Step-by-Step Guide to Make Your Motors Spin with PyTrinamic

The PyTrinamic library enables access to the TMC2209's advanced features like microstepping, StealthChop, and stallGuard through the UART interface.

#### Step 1: Install Required Libraries
```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
sudo pip3 install PyTrinamic pyserial
```

#### Step 2: Configure UART on Raspberry Pi
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

#### Step 3: Connect TMC2209 UART
Connect your TMC2209 to the Raspberry Pi:
- PDN_UART pin to RPi RX (GPIO15)
- PDN_UART pin to RPi TX (GPIO14) with a 1kΩ resistor in between
- Connect DIR, STEP, and EN pins as usual

#### Step 4: Run the PyTrinamic Script
Save the `tmc2209_pytrinamic.py` script to your Raspberry Pi, then run:

```bash
sudo python3 tmc2209_pytrinamic.py
```

This script will:
1. Configure the GPIO pins for your TMC2209 driver
2. Establish UART communication with the driver
3. Configure advanced settings like StealthChop mode, current, and microstepping
4. Rotate the motor 3200 steps clockwise (one full rotation with 1/16 microstepping)
5. Wait one second
6. Rotate the motor 3200 steps counterclockwise

#### Advanced Features for Telescope Control
For telescope operation, you may want to add these advanced features:

```python
# Silent StealthChop mode for quiet operation
tmc2209.set_spreadcycle(False)
tmc2209.set_stealthchop_threshold(1000000)  # Always use StealthChop

# Enable CoolStep for dynamic current adjustment
tmc2209.set_coolstep_threshold(1000)

# Configure stallGuard for sensorless homing
tmc2209.set_stallguard_threshold(5)  # Adjust sensitivity as needed
```

#### Troubleshooting PyTrinamic Issues
If you have issues with the PyTrinamic script:

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

#### Telescope-Specific Parameters
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

## Telescope Integration with INDI

### Telescope Control with INDI and KStars/Ekos

This section explains how to integrate your Raspberry Pi-controlled telescope with professional astronomy software for enhanced control and features.

#### What is INDI?

INDI (Instrument Neutral Distributed Interface) is an open-source protocol for controlling astronomical equipment. It provides a standard interface between software and astronomy hardware like:
- Telescopes and mounts
- Cameras
- Filter wheels
- Focusers
- Domes
- Weather stations

#### What is KStars/Ekos?

- **KStars**: A planetarium software that simulates the night sky
- **Ekos**: An advanced observatory control system built into KStars
- Together, they provide a complete astrophotography and telescope control solution

#### Benefits of Using INDI with Your DIY Telescope

- **Point-and-click astronomy**: Click on an object in KStars, and your telescope slews to it
- **Plate solving**: Automatically correct pointing errors
- **Equipment integration**: Control multiple devices from one interface
- **Automation**: Script observing sessions
- **Remote operation**: Control your telescope from inside your home or remotely

#### Installing INDI Server on Raspberry Pi

```bash
# Update your system
sudo apt update
sudo apt upgrade

# Install INDI core packages and common drivers
sudo apt install indi-full

# For minimal installation (alternative)
# sudo apt install indi-bin libindi-dev indi-basic
```

#### Installing KStars/Ekos

```bash
# On the Raspberry Pi (can be resource-intensive)
sudo apt install kstars-bleeding

# Or install on a separate computer and connect remotely
# For Ubuntu/Debian:
sudo apt install kstars-bleeding
```

#### Basic Configuration

##### Starting INDI Server

```bash
# Basic server start
indiserver indi_simulator_telescope

# For GPIO control (if using GPIO driver)
indiserver indi_gpiodriver

# To run in the background
indiserver -m 100 indi_gpiodriver &
```

##### Configuring GPIO Connection

If using the GPIO driver, you'll need to configure which pins connect to your TMC2209 drivers:

1. Edit or create the INDI configuration file:
   ```bash
   mkdir -p ~/.indi
   nano ~/.indi/indi_gpiodriver_sk.xml
   ```

2. Add configuration for your pins:
   ```xml
   <INDIDriver>
     <newSwitchVector device="GPIO" name="CONNECTION">
       <oneSwitch name="CONNECT">On</oneSwitch>
       <oneSwitch name="DISCONNECT">Off</oneSwitch>
     </newSwitchVector>
     <newNumberVector device="GPIO" name="GPIO_PINS">
       <oneNumber name="STEP_PIN">21</oneNumber>
       <oneNumber name="DIR_PIN">20</oneNumber>
       <oneNumber name="ENABLE_PIN">16</oneNumber>
     </newNumberVector>
   </INDIDriver>
   ```

#### Connecting KStars/Ekos

##### Setting Up a Profile in Ekos

1. Launch KStars
2. Open Ekos (Tools → Ekos or press F7)
3. Create a new profile:
   - Click "New Profile"
   - Name your profile (e.g., "RaspberryPi Telescope")
   - Set Mode to "Local" if running on the same machine as INDI server
   - Set Mode to "Remote" if running on a different computer

##### Connecting to INDI Server

###### Local Connection
1. In Ekos, select your profile and click "Start"
2. Go to the "INDI Control Panel"
3. Select your driver (e.g., "GPIO Driver")
4. Click "Connect" to establish communication

###### Remote Connection
1. In your profile, set Host to your Raspberry Pi's IP address
2. Set Port to the INDI server port (default: 7624)
3. Click "Start" to connect to the remote INDI server

#### Using the Custom INDI Driver

The `indi_telescope.py` script provides a custom INDI driver implementation for your TMC2209-controlled telescope.

1. Make the script executable:
   ```bash
   chmod +x indi_telescope.py
   ```

2. Run the script:
   ```bash
   sudo python3 indi_telescope.py
   ```

This will:
- Set up both RA and DEC motors
- Connect to the INDI server
- Start sidereal tracking
- Respond to commands from KStars/Ekos

#### Advanced Features

##### Plate Solving

Plate solving uses camera images to precisely determine telescope pointing:

1. Install required packages:
   ```bash
   sudo apt install indi-astrometry
   ```

2. In Ekos alignment module:
   - Take an image
   - Click "Solve" to determine exact pointing
   - "Sync" to update mount coordinates

##### Automated Meridian Flips

If using an equatorial mount:
1. Enable meridian flip in mount settings
2. Set flip offset (typically 5-15 minutes)
3. Ekos will automatically handle the flip during long sessions

##### Focus Control

If adding a motorized focuser:
1. Connect focuser in INDI Control Panel
2. Use Ekos Focus module to automatically find best focus

#### Troubleshooting

##### Common Issues

| Problem | Possible Solution |
|---------|------------------|
| INDI server won't start | Check for port conflicts, try different port with `-p PORT` |
| Can't connect to server | Verify IP address and firewall settings |
| Mount not moving | Check GPIO pin configuration and enable pin logic |
| Erratic movement | Verify correct microstep settings in TMC2209 |
| KStars crashes | Try running without OpenGL: `kstars --no-opengl` |

##### Logs and Debugging

```bash
# Run INDI server with verbose logging
indiserver -v indi_gpiodriver

# Save logs to file
indiserver -v indi_gpiodriver > indi_log.txt 2>&1
```

## Hardware Requirements

- Raspberry Pi 4 or 5
- NEMA17 stepper motors (at least 2 - one for RA and one for DEC)
- TMC2209 stepper motor drivers
- 12-24V power supply (sized appropriately for your motors)
- Jumper wires
- (Optional) Logic level shifter if using 3.3V to 5V conversion
- (Optional) Cooling for TMC2209 drivers during extended operation

## Wiring Diagrams

### Basic TMC2209 Wiring

| TMC2209 | Raspberry Pi GPIO (BCM) |
|---------|-------------------------|
| STEP    | 21                      |
| DIR     | 20                      |
| EN      | 16                      |
| GND     | GND                     |

### UART Configuration (for PyTrinamic)

| TMC2209 | Raspberry Pi GPIO (BCM) |
|---------|-------------------------|
| PDN_UART (RX) | GPIO14 (TX) with 1kΩ resistor |
| PDN_UART (TX) | GPIO15 (RX) |

### Motor Connections

| Motor Wire | TMC2209 |
|------------|---------|
| A1         | A1      |
| A2         | A2      |
| B1         | B1      |
| B2         | B2      |

## Troubleshooting

### Motor Issues
- **Motor doesn't move**: Check wiring connections and power supply
- **Motor vibrates but doesn't rotate**: Ensure all connections are correct
- **Unexpected rotation direction**: Swap your motor connections or change the direction parameter in code
- **Raspberry Pi unresponsive**: Ensure you have adequate power for both Pi and motors

### UART Issues
- **Can't communicate with driver**: Make sure UART is enabled in raspi-config
- **UART device not found**: Try alternative device paths (/dev/ttyS0, /dev/ttyAMA0)
- **UART communications errors**: Check wiring and make sure the 1kΩ resistor is in place

### INDI Issues
- **Can't see driver in INDI panel**: Check that the server is running with your driver loaded
- **Driver crashes**: Check the logs for errors and make sure all dependencies are installed
- **Network connectivity issues**: Verify IP addresses and that ports are open (7624 for INDI)