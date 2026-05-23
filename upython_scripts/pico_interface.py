"""
Upload this script to Pico as 'main.py'.
"""

import sys
import select
from time import sleep
from machine import Pin, PWM, WDT, freq, reset
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
# Variables
mode = 's'  # standby
# print("Pico is ready...")  # debug

# LOOP
try:
    while True:
        # Transmit data (TX)
        now_us = ticks_us()
        if ticks_diff(now_us, last_us) >= tx_period_us:
            motion_data = imu.read_data()
            out_msg = f"{motion_data['lin_acc_x']:.3f},{motion_data['ang_vel_z']:.3f}"
            print(out_msg)  # main.py will send this to computer
            last_us = now_us  # update last time stamp
        # Receive data (RX)
        is_waiting = pico_messenger.poll(0)  # check data in USB
        if is_waiting:
            in_msg = sys.stdin.readline().strip()  # take out whitespaces
            targ_vels = in_msg.split(",")  # get a list
            if len(targ_vels) == 2:
                try:
                    targ_lin_vel = float(targ_vels[0])
                    targ_ang_vel = float(targ_vels[1])
                    mobile_base.set_vels(targ_lin_vel, targ_ang_vel)
                except ValueError:
                    pass



        dutycycle_st = NEUTRAL_DUTY
        dutycycle_th = NEUTRAL_DUTY
        for msg, _ in event:
            if msg:
                wdt.feed()
                msg_line = msg.readline().rstrip()
                # print(f"Pico heard: {msg_line}")  # debug
                msg_parts = msg_line.split(",")
                # print(f"Pico heard: {msg_parts}")  # debug
                if len(msg_parts) == 3:
                    # print("Pico heard 2 parts")  # debug
                    try:
                        # Process driving actions
                        dutycycle_st = int(msg_parts[1])
                        dutycycle_th = int(msg_parts[2])
                        # Process LED actions
                        mode = msg_parts[0]
                        if mode is 'n':  # normal
                            r_led.value(1)
                            g_led.value(0)
                            b_led.value(1)
                        elif mode is 'r':  # recording
                            r_led.value(1)
                            g_led.value(1)
                            b_led.value(0)
                        elif mode is 'a':  # autopilot
                            r_led.value(0)
                            g_led.value(1)
                            b_led.value(0)
                        elif mode is 'p':  # pause
                            r_led.value(0)
                            g_led.value(0)
                            b_led.value(1)
                            dutycycle_st = NEUTRAL_DUTY
                            dutycycle_th = NEUTRAL_DUTY
                        else:  # error
                            r_led.value(0)
                            g_led.value(1)
                            b_led.value(1)
                            dutycycle_st = NEUTRAL_DUTY
                            dutycycle_th = NEUTRAL_DUTY
                        # print(f"Pico received command: {mode}, {dutycycle_st}, {dutycycle_th}") # debug
                        steering.duty_ns(dutycycle_st)
                        throttle.duty_ns(dutycycle_th)
                    except ValueError:
                        # print("ValueError!")  # debug
                        reset()
            else:
                throttle.duty_ns(NEUTRAL_DUTY)
                steering.duty_ns(NEUTRAL_DUTY)
                reset()
except Exception as e:
    # print('Pico reset')  # debug
    reset()
finally:
    # print('Pico reset')  # debug
    reset()
