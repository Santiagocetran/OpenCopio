# PWM and Stepper Drivers for Telescope Automation

## Benefits of PWM and Microstepping

For telescope automation, precision movement is critical. PWM (Pulse Width Modulation) enables microstepping, which offers several key advantages:

- **Higher Resolution**: Standard stepper motors move in 1.8° steps (200 steps/revolution), but microstepping can achieve 0.1° or finer movements
- **Smoother Motion**: Reduces vibration and jerky movements that could affect astronomical observations
- **Quieter Operation**: Significantly reduces motor noise during night viewing sessions
- **Better Efficiency**: Improved power management, especially during position holding

## L298N Limitations

While the L298N driver used in the current setup is adequate for initial testing, it has several limitations for advanced telescope control:

- Not designed specifically for stepper microstepping
- Relatively high power consumption and heat generation
- Limited resolution control
- Less precise current regulation

## Recommended Stepper Drivers for Upgrade

For improved telescope pointing and tracking precision, consider upgrading to these specialized stepper drivers:

| Driver  | Microstepping | Current | Features | Best For |
|---------|---------------|---------|----------|----------|
| A4988   | Up to 1/16    | 1A max  | - Simple to use<br>- Widely available<br>- Good documentation | Budget-conscious projects with moderate precision needs |
| DRV8825 | Up to 1/32    | 2.5A max | - Higher current capacity<br>- Better heat handling<br>- Higher resolution | Medium-sized telescopes requiring better precision |
| TMC2209 | Up to 1/256   | 2A max  | - Ultra-quiet operation<br>- StealthChop technology<br>- Higher efficiency<br>- Advanced features | High-precision applications where silent operation is important |

## Using the PWM Test Script with L298N

While waiting for upgraded drivers, you can experiment with PWM on the L298N using the provided `pwm_test.py` script:

### What the Script Does

The PWM test script applies pulse width modulation to the L298N control signals to:
- Adjust power delivered to the motor (controlling torque)
- Experiment with smoother acceleration and deceleration
- Test motor behavior at different power levels

> **Note**: This is not true microstepping (the L298N cannot do that), but rather simple power modulation.

### Running the PWM Test

1. Make the script executable:
   ```bash
   chmod +x pwm_test.py
   ```

2. Run the script:
   ```bash
   python pwm_test.py
   ```

3. Choose a mode when prompted:
   - Option 1: Runs a pre-defined sequence of tests
   - Option 2: Interactive mode for custom testing

### Interactive Mode Commands

- `c STEPS POWER` - Move STEPS steps clockwise at POWER% (1-100) 
- `a STEPS POWER` - Move STEPS steps counterclockwise at POWER%
- `s STEPS POWER DELAY` - Move with custom DELAY (in milliseconds)
- `q` - Quit the program

Example: `c 200 50` moves 200 steps clockwise at 50% power

### Wiring for PWM Testing

No additional wiring is needed! The script uses the same pin configuration as the original scripts:

| L298N | Raspberry Pi GPIO (BCM) |
|-------|-------------------------|
| IN1   | 17                      |
| IN2   | 18                      |
| IN3   | 27                      |
| IN4   | 22                      |

### What to Observe

- How different power levels affect motor torque
- Which power levels provide smoother operation
- How the motor sounds at different PWM settings
- Minimum power needed for reliable movement
- Maximum speed at different power levels

## Implementation Considerations

When upgrading to these drivers:

1. Each driver typically requires only 2-3 control pins from the Raspberry Pi (STEP, DIR, ENABLE)
2. Most support configuration of microstepping via jumpers or dedicated pins
3. Proper cooling may be required for extended operation
4. These drivers are significantly more power-efficient than the L298N

## Wiring Differences

Unlike the L298N which uses 4 pins to control stepping sequence directly:

```
# L298N requires explicitly sending the stepping sequence
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)
```

Dedicated stepper drivers simplify control to typically just two pins:

```
# For dedicated stepper drivers
GPIO.output(DIR_PIN, GPIO.HIGH)  # Set direction
for _ in range(steps):
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(pulse_delay)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(pulse_delay)
```

This simplification makes code more maintainable while achieving higher precision.