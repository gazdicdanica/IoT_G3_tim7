import time
import random


def run_dms_simulator(delay, callback, stop_event, name, runsOn):
    while True:
        time.sleep(delay)
        callback(random.randint(0, 100)>50, name, True, runsOn)
        if stop_event.is_set():
            break