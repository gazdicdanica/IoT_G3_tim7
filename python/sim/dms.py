import time
import random


def generate_door_unlocked():
    while True:
        yield random.choice([True, False])

def run_dms_simulator(delay, callback, stop_event, name, runsOn):
    door_unlocked_generator = generate_door_unlocked()
    for door_unlocked in door_unlocked_generator:
        time.sleep(delay)
        callback(door_unlocked, name, True, runsOn)
        if stop_event.is_set():
            break