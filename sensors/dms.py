import RPi.GPIO as GPIO
import time

class DMS:
    def __init__(self, name, pins):
        self.name = name
        self.pins = pins

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
            print(characters[0])
        if(GPIO.input(self.pins[5]) == 1):
            print(characters[1])
        if(GPIO.input(self.pins[6]) == 1):
            print(characters[2])
        if(GPIO.input(self.pins[7]) == 1):
            print(characters[3])
        GPIO.output(line, GPIO.LOW)


# TODO: implement this
def run_dms_loop(self, delay, callback, stop_event, name, runsOn):
    while True:
        self.readLine(self.pins[0], ["1","2","3","A"])
        self.readLine(self.pins[1], ["4","5","6","B"])
        self.readLine(self.pins[2], ["7","8","9","C"])
        self.readLine(self.pins[3], ["*","0","#","D"])
        time.sleep(0.2)


    