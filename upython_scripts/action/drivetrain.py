from machine import Pin, PWM

NEUTRAL_PULSE_WIDTH = 1_500_000  # nanosec


class Drivetrain:
    def __init__(self, steering_pin_id=16, throttle_pin_id=17):
        self.steering = PWM(Pin(steering_pin_id))
        self.steering.freq(50)
        self.throttle = PWM(Pin(throttle_pin_id))
        self.throttle.freq(50)
        self.stop()

    def set_angle(self, pulse_width_ns):
        """
        Set angle of servo motor
        """
        self.steering.duty_ns(pulse_width_ns)

    def set_speed(self, pulse_width_ns):
        """
        Set speed of propelling motor via ESC
        """
        self.throttle.duty_ns(pulse_width_ns)

    def stop(self):
        self.set_angle(NEUTRAL_PULSE_WIDTH)
        self.set_speed(NEUTRAL_PULSE_WIDTH)


if __name__ == "__main__":
    from utime import sleep

    # SETUP
    drvtrn = Drivetrain(steering_pin_id=16, throttle_pin_id=17)
    ang_pw = NEUTRAL_PULSE_WIDTH
    spd_pw = NEUTRAL_PULSE_WIDTH
    set_counts = 0
    # SAFETY CHECK
    is_lifted = input("Is anything making contact to any wheel of BearCar? (Y/n)")
    while is_lifted is not "n":
        print("Please lift BearCar up and make sure the wheels are in the air!")
        is_lifted = input("Is anything making contact to any wheel of BearCar? (Y/n)")
    print(
        "For safety reasons, input values will be clamped in a limited range around 1_500_000 nanosec."
    )

    # LOOP
    while set_counts < 3:
        print(f"Set angle and speed ({set_counts + 1}/8)")
        raw_input = input(
            "Please input PWM signals' pulse width separated by ',' (Example: 1600000,1350000):"
        )
        # print(raw_input)  # debug
        data = raw_input.split(",")
        # print(data)  # debug
        if len(data) == 2:
            try:
                ang_pw = int(data[0])
                ang_pw = max(1_100_000, min(ang_pw, 1_900_000))
                print(f"Set angle pulse width: {ang_pw} nanosec")
                spd_pw = int(data[1])
                spd_pw = max(1_400_000, min(spd_pw, 1_600_000))
                print(f"Set speed pulse width: {spd_pw} nanosec")
                drvtrn.set_angle(ang_pw)
                drvtrn.set_speed(spd_pw)
            except ValueError:
                print(
                    "Cannot convert input to valid pulse width values, please check your input."
                )
                set_counts += 1
                continue
        else:
            print("Please input 2 values separated by a Comma (,).")
            set_counts += 1
            continue
        for i in reversed(range(3)):
            print(i + 1)
            sleep(1)
        drvtrn.set_angle(NEUTRAL_PULSE_WIDTH)
        drvtrn.set_speed(NEUTRAL_PULSE_WIDTH)
        set_counts += 1
