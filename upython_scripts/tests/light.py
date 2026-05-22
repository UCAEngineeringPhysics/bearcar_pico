from machine import Pin, reset
from time import sleep


# SETUP
# Config the common anode LED
red = Pin(21, Pin.OUT)
red.value(0)  # 0 = off; 1 = on
green = Pin(20, Pin.OUT)
green.value(0)
blue = Pin(19, Pin.OUT)
blue.value(0)
# leds = (g, r, b)
leds = (red, green, blue)

# LOOP
for i in range(len(leds)):
    for _ in range(4):
        leds[i].toggle()
        sleep(0.5)

print("Yellow")
leds[0].value(1)
leds[1].value(1)
leds[2].value(0)
sleep(1)
print("Cyan")
leds[0].value(0)
leds[1].value(1)
leds[2].value(1)
sleep(1)
print("Purple")
leds[0].value(1)
leds[1].value(0)
leds[2].value(1)
sleep(1)
# reset()
reset()
