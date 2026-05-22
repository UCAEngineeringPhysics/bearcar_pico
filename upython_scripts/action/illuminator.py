from machine import Pin


class Illuminator:
    def __init__(self, red_pin_id=21, green_pin_id=20, blue_pin_id=19) -> None:
        self.red_led = Pin(red_pin_id, Pin.OUT)
        self.green_led = Pin(green_pin_id, Pin.OUT)
        self.blue_led = Pin(blue_pin_id, Pin.OUT)

    def glow(self, mode=""):
        if mode == "e":  # error: red
            self.red_led.value(1)
            self.green_led.value(0)
            self.blue_led.value(0)
        elif mode == "n":  # normal: green
            self.red_led.value(0)
            self.green_led.value(1)
            self.blue_led.value(0)
        elif mode == "r":  # recording: blue
            self.red_led.value(0)
            self.green_led.value(0)
            self.blue_led.value(1)
        elif mode == "a":  # autopilot: purple
            self.red_led.value(1)
            self.green_led.value(0)
            self.blue_led.value(1)
        elif mode == "p":  # pause: yellow
            self.red_led.value(1)
            self.green_led.value(1)
            self.blue_led.value(0)
        elif mode == "s":  # standby: cyan
            self.red_led.value(0)
            self.green_led.value(1)
            self.blue_led.value(1)
        else:
            self.red_led.value(0)
            self.green_led.value(0)
            self.blue_led.value(0)


if __name__ == "__main__":
    from utime import sleep

    bulb = Illuminator(red_pin_id=21, green_pin_id=20, blue_pin_id=19)
    # Loop over all modes
    modes = "aenprs" + "z"
    for m in modes:
        bulb.glow(mode=m)
        sleep(1)
