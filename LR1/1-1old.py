import RPi.GPIO as GPIO
import time

LED_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_pin, GPIO.OUT)

while True:
    GPIO.output(LED_pin, GPIO.HIGH)