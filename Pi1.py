import threading
import time
from scripts.load_settings import load_settings
from components.dht11 import run_dht
from components.pir import run_pir
from components.dl import run_dl
from components.hcsr04 import run_ultrasonic
from components.ds import run_ds
from components.dms import run_dms
from components.db import run_db
from queue import Queue
import paho.mqtt.publish as publish


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

light_queue = Queue()
buzzer_queue = Queue()

def run_user_input_threads(threads, stop_event):
    input_thread = threading.Thread(target=user_input_thread, args=(stop_event,))
    input_thread.start()
    threads.append(input_thread)

def user_input_thread(stop_event):
    global light_queue
    global buzzer_queue

    while True:
        user_input = input()
        if user_input == 'l':
            light_queue.put(user_input)
        if user_input == 'b':
            buzzer_queue.put(user_input)
        time.sleep(0.1)
        if stop_event.is_set():
            break

if __name__ == "__main__":
    print("*** G3 Tim7 ***")
    threads = []
    stop_event = threading.Event()
    pi1_settings = load_settings("1")

    try:
        dht1_settings = pi1_settings['RDHT1']
        dht2_settings = pi1_settings['RDHT2']
        rpir1_settings = pi1_settings['RPIR1']
        rpir2_settings = pi1_settings['RPIR2']
        dpir1_settings = pi1_settings['DPIR1']
        dus1_settings = pi1_settings['DUS1']
        ds1_settings = pi1_settings['DS1']
        dms_settings = pi1_settings['DMS']
        dl_settings = pi1_settings['DL']
        db_settings = pi1_settings['DB']

        run_user_input_threads(threads, stop_event)

        run_dht(dht1_settings, threads, stop_event)
        run_dht(dht2_settings, threads, stop_event)
        
        run_pir(rpir1_settings, threads, stop_event)
        run_pir(rpir2_settings, threads, stop_event)
        run_pir(dpir1_settings, threads, stop_event)
        
        run_ds(ds1_settings, threads, stop_event)
        run_dms(dms_settings, threads, stop_event)
        run_dl(light_queue, dl_settings, threads, stop_event)
        run_db(buzzer_queue, db_settings, threads, stop_event)
        
        run_ultrasonic(dus1_settings, threads, stop_event)

        while True:
            time.sleep(5)


    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()