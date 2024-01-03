import RPi.GPIO as GPIO
import time


class RGB:
    def __init__(self, name, r_pin, g_pin, b_pin) -> None:
        self.name = name
        self.R_pin = r_pin
        self.G_pin = g_pin
        self.B_pin = b_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.R_pin, GPIO.OUT)
        GPIO.setup(self.G_pin, GPIO.OUT)
        GPIO.setup(self.B_pin, GPIO.OUT)

    def turn_on(self):
        self.isOn = True
        self.white()

    def turn_off(self):
        self.isOn = False
        GPIO.output(self.R_pin, GPIO.LOW)
        GPIO.output(self.G_pin, GPIO.LOW)
        GPIO.output(self.B_pin, GPIO.LOW)
    
    def white(self):
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.HIGH)
        
    def red(self):
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.LOW)
        GPIO.output(self.B_pin, GPIO.LOW)

    def green(self):
        GPIO.output(self.R_pin, GPIO.LOW)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.LOW)
        
    def blue(self):
        GPIO.output(self.R_pin, GPIO.LOW)
        GPIO.output(self.G_pin, GPIO.LOW)
        GPIO.output(self.B_pin, GPIO.HIGH)
        
    def yellow(self):
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.LOW)
        
    def purple(self):
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.LOW)
        GPIO.output(self.B_pin, GPIO.HIGH)
        
    def light_blue(self):
        GPIO.output(self.R_pin, GPIO.LOW)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.HIGH)

def run_rgb_loop(input_queue, rgb, delay, stop_event, name, runsOn):
    while True:
        if input_queue.qsize() > 0:
            user_input = input_queue.get()
            if user_input == "x":
                rgb.turn_off()
                #TODO: da li treba callback?
            elif user_input == "w":
                rgb.white()
            elif user_input == "r":
                rgb.red()
            elif user_input == "g":
                rgb.green()
            elif user_input == "b":
                rgb.blue()
            elif user_input == "y":
                rgb.yellow()
            elif user_input == "p":
                rgb.purple()
            elif user_input == "lb":
                rgb.light_blue()
        if stop_event.is_set():
            break
        time.sleep(delay)
