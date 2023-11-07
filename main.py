import threading
import time
from scripts.load_settings import load_settings
from components.dht11 import run_dht
from components.pir import run_pir
from components.hcsr04 import run_ultrasonic


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


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

        run_dht(dht1_settings, threads, stop_event)
        run_dht(dht2_settings, threads, stop_event)

        run_pir(rpir1_settings, threads, stop_event)
        run_pir(rpir2_settings, threads, stop_event)
        run_pir(dpir1_settings, threads, stop_event)

        run_ultrasonic(dus1_settings, threads, stop_event)
        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()