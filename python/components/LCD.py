#!/usr/bin/env python3

from sensors.LCD.PCF8574 import PCF8574_GPIO
from sensors.LCD.Adafruit_LCD1602 import Adafruit_CharLCD
import paho.mqtt.client as mqtt

from time import sleep, strftime
from datetime import datetime
import json

mqtt_client = mqtt.Client()
temp = 0
humidity = 0
HOSTNAME = ""
PORT = 0

def on_connect(client, userdata, flags, rc):
    client.subscribe("GDHT_Data")
 
def on_message(client, userdata, msg):
    global temp, humidity
    data = json.loads(msg.payload.decode('utf-8'))
    temp = data["temperature"]
    humidity = data["humidity"]

def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    
def run_lcd_loop(settings, threads, stop_event):
    global temp, humidity, HOSTNAME, PORT
    HOSTNAME = settings['hostname']
    PORT = settings['port']
    mqtt_client.connect(HOSTNAME, PORT, 60)
    mqtt_client.loop_start()
    if settings['simulated']:
        print("Starting simulated gyro")
        print("Temp: ", temp, "\n", "Humid: ", humidity)
    else:
        PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        try:
            mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)
                
        lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
        mcp.output(3,1)     # turn on LCD backlight
        lcd.begin(16,2)     # set number of LCD lines and columns
        while(True):   
            global temp, humidity      
            #lcd.clear()
            lcd.setCursor(0,0)  # set cursor position
            lcd.message( 'Temp: ' + temp + '\n' + 'Humid: ' + humidity)
            print(temp, "_", humidity)
            sleep(1)   
