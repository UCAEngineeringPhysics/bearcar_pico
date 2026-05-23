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
tx_period_us = 16_667 # 60 Hz
smooth_coeff = 0.85  # low-pass filter coefficient for accel
deadzone_acc = 0.05  # m/s^2 (Ignore micro-vibrations)
# Variables
filtered_acc_x = 0.0  # init accel
lin_vel_x = 0.0
mode = 's'  # standby
# print("Pico is ready...")  # debug

# LOOP
last_us = ticks_us()
while True:
    # Transmit data (TX)
    now_us = ticks_us()
    if ticks_diff(now_us, last_us) >= tx_period_us:
        # Extract linear velocity on x and angular velocity on z
        motion_data = imu.read_data()
        filtered_acc_x = (smooth_coeff * filtered_acc_x) + ((1 - smooth_coeff) * motion_data['lin_acc_x'])
        if abs(filtered_acc_x) < deadzone_acc:
            filtered_acc_x = 0.0
            lin_vel_x *= 0.05 
            if abs(lin_vel_x) < 0.01: v_x = 0.0
        lin_vel_x += filtered_acc_x * tx_period_us * 1e-6
        out_msg = f"{lin_vel_x:.3f},{motion_data['ang_vel_z']:.3f}"
        print(out_msg)  # main.py will send this to computer
        last_us = now_us  # update last time stamp
    # Receive data (RX)
    is_waiting = messenger.poll(0)  # check data in USB
    if is_waiting:
        in_msg = sys.stdin.readline().strip().split(",")
        if len(in_msg) == 3:
            try:
                rgb_led.glow(in_msg[0])
                drivetrain.set_angle(int(in_msg[1]))
                drivetrain.set_speed(int(in_msg[2]))
            except ValueError:
                pass
        else:
            rgb_led.glow('e')
            drivetrain.stop()
