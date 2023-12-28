import RPi.GPIO as GPIO
import time

class FourSegment:
    num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}

    def __init__(self, name, segments, digits):
        self.name = name
        self.segments = segments
        self.digits = digits
        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        for digit in digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)        


    def show_time(self):
        try:
            while True:
                n = time.ctime()[11:13]+time.ctime()[14:16]
                s = str(n).rjust(4)
                for digit in range(4):
                    for loop in range(0,7):
                        GPIO.output(self.segments[loop], self.num[s[digit]][loop])
                        if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
                            GPIO.output(25, 1)
                        else:
                            GPIO.output(25, 0)
                    GPIO.output(self.digits[digit], 0)
                    # if wake_up:
                    #     time.sleep(0.5)
                    # else:
                    time.sleep(0.001)
                    GPIO.output(self.digits[digit], 1)
                
                
        finally:
            GPIO.cleanup()


