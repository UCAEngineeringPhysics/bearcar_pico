from machine import Pin, PWM, reset
from time import sleep

# SAFETY CHECK
is_lifted = input("Is anything making contact to any wheel of BearCar? (Y/n)")
while not is_lifted == "n":
    print("Please lift BearCar up and make sure the wheels are in the air!")
    is_lifted = input("Is anything making contact to any wheel of BearCar? (Y/n)")
print("Please calibrate ESC throttle follow the steps below:")
print("1. Turn off ESC.")
print("2. Unplug Pico.")
print("3. Plug Pico back in.")
print("4. Turn ESC back on.")
print("5. Run this MicroPython script.")

# SETUP
throttle = PWM(Pin(17))
throttle.freq(50)
# Range constants
DUTY_NEUTRAL = 1_500_000  # nanoseconds
DUTY_FMAX = 2_000_000
# TODO: figure out if max reverse is configurable
# Set neutral throttle's dutycycle
throttle.duty_ns(DUTY_NEUTRAL)
sleep(0.5)

# LOOP
try:
    # Set max forward dutycycle
    throttle.duty_ns(DUTY_FMAX)
    sleep(0.5)
    # Set throttle's dutycycle back to neutral
    throttle.duty_ns(DUTY_NEUTRAL)
    sleep(2)
except:
    print("Exception!")
finally:
    print("\n\u2713Throttle is calibrated\u2713\n")
    print("Calibration succeeded, if you heard a long beep followed by 2 short beeps.")
    print("If not, repeat and follow the instructions carefully.")
    sleep(0.1)
    reset()
