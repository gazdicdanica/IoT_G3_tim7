import RPi.GPIO as GPIO

class DoorSensor:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

    def is_door_open(self):
        GPIO.setup(self.pin, GPIO.IN)
        return GPIO.input(self.pin) == GPIO.HIGH

    