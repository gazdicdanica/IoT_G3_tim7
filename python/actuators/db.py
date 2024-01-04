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
    
def run_db_loop(should_turn_on, input_queue, db, delay, callback, stop_event, name, runsOn):
    alarm_on = False
    while True:
        if should_turn_on.qsize() > 0:
            alarm_on = should_turn_on.get()
            if alarm_on:
                db.turn_on()
                callback(True, name, False, runsOn)
            else:
                db.turn_off()
                callback(False, name, False, runsOn)
        elif input_queue.qsize() > 0:
            user_input = input_queue.get()
            if user_input == 'z':
                if db.is_buzzer_on():
                    db.turn_off()
                    callback(False, name, False, runsOn)
                else:
                    db.turn_on()
                    callback(True, name, False, runsOn)
        if stop_event.is_set():
            break
        if alarm_on:
            alarm_on = False
            time.sleep(10)
            print("Buzzer ", name, " OFF")
            db.turn_off()
            callback(False, name, False, runsOn)
        else:
            time.sleep(delay)