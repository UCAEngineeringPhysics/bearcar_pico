"""
Upload this script to Pico as 'main.py'.
"""

import sys
from utime import ticks_us, ticks_diff
import select
from time import sleep
from machine import freq, reset
from action.drivetrain import Drivetrain
from action.illuminator import Illuminator
from perception.inertial_sensor import MPU6050

# SETUP
# Overclock
freq(240_000_000)  # Pico 2 original: 150_000_000
# Instantiate components on the board
rgb_led = Illuminator(red_pin_id=21, green_pin_id=20, blue_pin_id=19)
driver = Drivetrain(steering_pin_id=16, throttle_pin_id=17)
imu = MPU6050(i2c_channel=1, scl_id=15, sda_id=14, i2c_addr=0x68)
# Config USB messenger
messenger = select.poll()
messenger.register(sys.stdin, select.POLLIN)
# Constants
tx_period_us = 16_667  # 60 Hz
# Variables
mode = "s"  # standby
# print("Pico is ready...")  # debug

# LOOP
last_us = ticks_us()
while True:
    # Transmit data (TX)
    now_us = ticks_us()
    if ticks_diff(now_us, last_us) >= tx_period_us:
        # Extract angular velocity on z
        motion_data = imu.read_data()
        out_msg = f"{motion_data['ang_vel_z']:.3f}"
        print(out_msg)  # main.py will send this to computer
        last_us = now_us  # update last time stamp
    # Receive data (RX)
    is_waiting = messenger.poll(0)  # check data in USB
    if is_waiting:
        in_msg = sys.stdin.readline().strip().split(",")
        if len(in_msg) == 3:
            try:
                rgb_led.glow(in_msg[0])
                driver.set_angle(int(in_msg[1]))
                driver.set_speed(int(in_msg[2]))
            except ValueError:
                rgb_led.glow("e")
                driver.stop()
        else:
            rgb_led.glow("e")
            driver.stop()
