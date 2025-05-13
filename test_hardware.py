#!/usr/bin/env python3
"""
Test script to verify the complete telescope setup
"""
import os
import sys
import time
import RPi.GPIO as GPIO

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import RPi.GPIO
        print("✓ RPi.GPIO installed")
    except ImportError:
        print("✗ RPi.GPIO not installed")
    
    try:
        from pytrinamic.connections import ConnectionManager
        print("✓ PyTrinamic installed")
    except ImportError:
        print("✗ PyTrinamic not installed")
    
    try:
        import PyIndi
        print("✓ PyIndi installed")
    except ImportError:
        print("✗ PyIndi not installed")

def test_gpio_access():
    """Test if the script can access GPIO pins"""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(21, GPIO.LOW)
        GPIO.cleanup()
        print("✓ GPIO access working")
        return True
    except Exception as e:
        print(f"✗ GPIO access failed: {e}")
        return False

def main():
    print("Telescope Hardware Test")
    print("======================")
    
    print("\nChecking dependencies:")
    check_dependencies()
    
    print("\nTesting GPIO access:")
    test_gpio_access()
    
    print("\nChecking UART configuration:")
    if os.path.exists("/dev/ttyS0"):
        print("✓ UART device /dev/ttyS0 exists")
    else:
        print("✗ UART device /dev/ttyS0 not found")
    
    print("\nTest complete!")

if __name__ == "__main__":
    main()