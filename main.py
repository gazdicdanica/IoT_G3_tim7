import threading
import time
from scripts.load_settings import load_settings
from components.dht11 import run_dht


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

        run_dht(dht1_settings, threads, stop_event)
        run_dht(dht2_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()