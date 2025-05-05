# Telescope Control with INDI and KStars/Ekos

This guide explains how to integrate your Raspberry Pi-controlled telescope (using TMC2209 drivers and NEMA 17 stepper motors) with professional astronomy software for enhanced control and features.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Basic Configuration](#basic-configuration)
- [Connecting KStars/Ekos](#connecting-kstarsekos)
- [Creating a Custom Driver](#creating-a-custom-driver)
- [Telescope Operation](#telescope-operation)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

## Introduction

### What is INDI?

INDI (Instrument Neutral Distributed Interface) is an open-source protocol for controlling astronomical equipment. It provides a standard interface between software and astronomy hardware like:
- Telescopes and mounts
- Cameras
- Filter wheels
- Focusers
- Domes
- Weather stations

### What is KStars/Ekos?

- **KStars**: A planetarium software that simulates the night sky
- **Ekos**: An advanced observatory control system built into KStars
- Together, they provide a complete astrophotography and telescope control solution

### Benefits of Using INDI with Your DIY Telescope

- **Point-and-click astronomy**: Click on an object in KStars, and your telescope slews to it
- **Plate solving**: Automatically correct pointing errors
- **Equipment integration**: Control multiple devices from one interface
- **Automation**: Script observing sessions
- **Remote operation**: Control your telescope from inside your home or remotely

## Installation

### Installing INDI Server on Raspberry Pi

```bash
# Update your system
sudo apt update
sudo apt upgrade

# Install INDI core packages and common drivers
sudo apt install indi-full

# For minimal installation (alternative)
# sudo apt install indi-bin libindi-dev indi-basic
```

### Installing KStars/Ekos

```bash
# On the Raspberry Pi (can be resource-intensive)
sudo apt install kstars-bleeding

# Or install on a separate computer and connect remotely
# For Ubuntu/Debian:
sudo apt install kstars-bleeding
```

## Basic Configuration

### Starting INDI Server

```bash
# Basic server start
indiserver indi_simulator_telescope

# For GPIO control (if using GPIO driver)
indiserver indi_gpiodriver

# To run in the background
indiserver -m 100 indi_gpiodriver &
```

### Configuring GPIO Connection

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

## Connecting KStars/Ekos

### Setting Up a Profile in Ekos

1. Launch KStars
2. Open Ekos (Tools → Ekos or press F7)
3. Create a new profile:
   - Click "New Profile"
   - Name your profile (e.g., "RaspberryPi Telescope")
   - Set Mode to "Local" if running on the same machine as INDI server
   - Set Mode to "Remote" if running on a different computer

### Connecting to INDI Server

#### Local Connection
1. In Ekos, select your profile and click "Start"
2. Go to the "INDI Control Panel"
3. Select your driver (e.g., "GPIO Driver")
4. Click "Connect" to establish communication

#### Remote Connection
1. In your profile, set Host to your Raspberry Pi's IP address
2. Set Port to the INDI server port (default: 7624)
3. Click "Start" to connect to the remote INDI server

## Creating a Custom Driver

For better integration, you may want to create a custom INDI driver for your TMC2209-controlled telescope.

### Prerequisites

```bash
sudo apt install build-essential cmake libindi-dev
git clone https://github.com/indilib/indi.git
```

### Basic Driver Structure

1. Use an existing driver as a template (e.g., `indi-gpiodriver`)
2. Create these key files:
   - `mytelescope.cpp` - Main driver implementation
   - `mytelescope.h` - Header file
   - `CMakeLists.txt` - Build configuration

3. Implement these essential functions:
   - `ISGetProperties` - Define telescope properties
   - `initProperties` - Initialize properties
   - `updateProperties` - Update properties when connection state changes
   - `ISNewNumber`, `ISNewSwitch`, etc. - Handle property changes
   - `MoveNS`, `MoveWE`, `GoTo` - Implement telescope movement

### Compiling Your Driver

```bash
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make
sudo make install
```

## Telescope Operation

### Basic Controls in Ekos

1. **Mount Control Panel**: 
   - Provides manual telescope control
   - Slew, track, park/unpark functions

2. **Alignment Module**:
   - Calibrate your telescope pointing
   - Supports 1, 2, or 3-star alignment

3. **Scheduler**:
   - Set up automated observing sequences
   - Define targets, durations, and conditions

### Configuring Mount Parameters

In the INDI Control Panel:
1. Set motor steps per revolution
2. Configure gear ratios
3. Set maximum slew rates
4. Define mount limits

## Advanced Features

### Plate Solving

Plate solving uses camera images to precisely determine telescope pointing:

1. Install required packages:
   ```bash
   sudo apt install indi-astrometry
   ```

2. In Ekos alignment module:
   - Take an image
   - Click "Solve" to determine exact pointing
   - "Sync" to update mount coordinates

### Automated Meridian Flips

If using an equatorial mount:
1. Enable meridian flip in mount settings
2. Set flip offset (typically 5-15 minutes)
3. Ekos will automatically handle the flip during long sessions

### Focus Control

If adding a motorized focuser:
1. Connect focuser in INDI Control Panel
2. Use Ekos Focus module to automatically find best focus

## Troubleshooting

### Common Issues

| Problem | Possible Solution |
|---------|------------------|
| INDI server won't start | Check for port conflicts, try different port with `-p PORT` |
| Can't connect to server | Verify IP address and firewall settings |
| Mount not moving | Check GPIO pin configuration and enable pin logic |
| Erratic movement | Verify correct microstep settings in TMC2209 |
| KStars crashes | Try running without OpenGL: `kstars --no-opengl` |

### Logs and Debugging

```bash
# Run INDI server with verbose logging
indiserver -v indi_gpiodriver

# Save logs to file
indiserver -v indi_gpiodriver > indi_log.txt 2>&1
```

## Additional Resources

- [INDI Library Documentation](https://www.indilib.org/developers.html)
- [KStars Handbook](https://docs.kde.org/trunk5/en/kstars/kstars/index.html)
- [Ekos Tutorial](https://www.indilib.org/about/ekos.html)
- [INDI Forums](https://indilib.org/forum.html)
- [Raspberry Pi Astronomy Projects](https://astroberry.io/docs/)

---

This README covers the basics of integrating your TMC2209-controlled telescope with astronomy software. As you get more comfortable with the system, you can explore additional features like autoguiding, automated imaging sequences, and weather monitoring.
