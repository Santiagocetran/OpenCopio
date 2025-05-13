# NEMA17 Stepper Motor Control with Raspberry Pi

This repository contains simple Python scripts for controlling NEMA17 stepper motors using L298N motor controllers with Raspberry Pi 4/5, intended for DIY telescope automation.

## Hardware Requirements

- Raspberry Pi 4 or 5
- NEMA17 stepper motor
- L298N motor controller
- 12V power supply for the L298N
- Jumper wires

## Wiring Instructions

Connect your L298N controller to the Raspberry Pi:

| L298N | Raspberry Pi GPIO (BCM) |
|-------|-------------------------|
| IN1   | 17                      |
| IN2   | 18                      |
| IN3   | 27                      |
| IN4   | 22                      |

Power connections:
- Connect external 12V power supply to L298N power inputs
- Connect L298N ground to Raspberry Pi ground

## Installation

1. Clone this repository to your Raspberry Pi:
   ```
   git clone https://github.com/yourusername/stepper-motor-control.git
   cd stepper-motor-control
   ```

2. Make the scripts executable:
   ```
   chmod +x stepper_control.py quick_test.py
   ```

3. Install required Python package (RPi.GPIO):
   ```
   pip install RPi.GPIO
   ```
   
   Note: On Raspberry Pi OS, RPi.GPIO usually comes pre-installed.

## Usage

### Quick Test Script

To perform a quick test of your motor (one full rotation in each direction):

```bash
python quick_test.py
```

### Interactive Control Script

For interactive control of your stepper motor:

```bash
python stepper_control.py
```

Available commands:
- `c 200` - Move 200 steps clockwise 
- `a 200` - Move 200 steps counterclockwise
- `q` - Quit the program

## Customization

- Adjust GPIO pin numbers in the scripts if your wiring differs
- Modify `STEP_DELAY` (default: 0.003) to change motor speed:
  - Lower value = faster rotation
  - Higher value = slower rotation
- For different NEMA17 models, you may need to adjust the number of steps in quick_test.py (default: 200 steps per revolution)

## Troubleshooting

- **Motor doesn't move**: Check wiring connections and power supply
- **Motor vibrates but doesn't rotate**: Ensure all four connections are correct
- **Unexpected rotation direction**: Swap your motor connections or change the direction parameter in code
- **Raspberry Pi unresponsive**: Ensure you have adequate power for both Pi and motors

## License

MIT