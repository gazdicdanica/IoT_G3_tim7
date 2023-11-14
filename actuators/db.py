import RPi.GPIO as GPIO
import time

class DoorBuzzer:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def is_buzzer_on(self):
        return GPIO.input(self.pin) == GPIO.HIGH
    
def run_db_loop(input_queue, db, delay, callback, stop_event, name):
    while True:
        if input_queue.qsize() > 0:
            user_input = input_queue.get()
            if user_input == 'b':
                if db.is_buzzer_on():
                    db.turn_off()
                    callback(False, name)
                else:
                    db.turn_on()
                    callback(True, name)
        if stop_event.is_set():
            break
        time.sleep(delay)