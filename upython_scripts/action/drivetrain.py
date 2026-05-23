from machine import Pin, PWM

NEUTRAL_PULSE_WIDTH = 1_500_000 # nanosec

class Drivetrain:
    def __init__(self): -> None
        self.steering = PWM(Pin(16))
        self.steering.freq(50)
        self.throttle = PWM(Pin(17))
        self.throttle.freq(50)
        self.stop()

    def set_angle(self, pulse_width_ns):
        """
        Set heading angle via the servo motor
        """
        self.steering.duty_ns(pulse_width_ns)

    def set_speed(self, pulse_width_ns):
        """
        Set speed via the ESC
        """
        self.throttle.duty_ns(pulse_width_ns)

    def stop(self):
        self.set_angle(NEUTRAL_PULSE_WIDTH)
        self.set_speed(NEUTRAL_PULSE_WIDTH)

