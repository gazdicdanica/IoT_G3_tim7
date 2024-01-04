import RPi.GPIO as GPIO
import time

class DMS:
    def __init__(self, name, pins, pincode):
        self.name = name
        self.pins = pins
        self.pincode = pincode

        GPIO.setup(pins[0], GPIO.OUT)
        GPIO.setup(pins[1], GPIO.OUT)
        GPIO.setup(pins[2], GPIO.OUT)
        GPIO.setup(pins[3], GPIO.OUT)

        GPIO.setup(pins[4], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pins[5], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pins[6], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pins[7], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def readLine(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.pins[4]) == 1):
            return characters[0]
        if(GPIO.input(self.pins[5]) == 1):
            return characters[1]
        if(GPIO.input(self.pins[6]) == 1):
            return characters[2]
        if(GPIO.input(self.pins[7]) == 1):
            return characters[3]
        GPIO.output(line, GPIO.LOW)


# TODO: implement this
def run_dms_loop(self, delay, callback, stop_event, name, runsOn):
    a = None
    b = None
    c = None 
    d = None
    while True:
        a = self.readLine(self.pins[0], ["1","2","3","A"])
        b = self.readLine(self.pins[1], ["4","5","6","B"])
        c = self.readLine(self.pins[2], ["7","8","9","C"])
        d = self.readLine(self.pins[3], ["*","0","#","D"])
        if a and b and c and d:
            code = a + b + c + d
            if code == self.pincode:
                callback(False, name, False, runsOn)
            else:
                callback(True, name, False, runsOn)
                a = None
                b = None
                c = None
                d = None
        
        time.sleep(0.2)
        if stop_event.is_set():
            break

    