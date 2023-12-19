import RPi.GPIO as GPIO
import time

class DoorLight:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def is_light_on(self):
        return GPIO.input(self.pin) == GPIO.HIGH
    
def run_dl_loop(input_queue, dl, delay, callback, stop_event, name, runsOn):
    while True:
        if input_queue.qsize() > 0:
            user_input = input_queue.get()
            if user_input == 'l':
                if dl.is_light_on():
                    dl.turn_off()
                    callback(False, name, False, runsOn)
                else:
                    dl.turn_on()
                    callback(True, name, False, runsOn)
        if stop_event.is_set():
            break
        time.sleep(delay)