import RPi.GPIO as GPIO
import time

class PIR:
    def __init__(self, name, pin):
        self.pin = pin
        self.name = name

    def motionDetected(self):
        GPIO.setup(self.pin, GPIO.IN)
        return GPIO.input(self.pin)
