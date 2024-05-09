import os
import time

def led_init():
	os.system("echo none >/sys/class/leds/led0/trigger")

def led_on():
	os.system("echo 1 >/sys/class/leds/led0/brightness")

def led_off():
	os.system("echo 0 >/sys/class/leds/led0/brightness")



led_init()

while True:
	led_on()
	time.sleep(1)
	led_off()
	time.sleep(1)