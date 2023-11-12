import time
import random
from prettytable import PrettyTable

dms_table = PrettyTable(["Sensor", "TimeStamp", "Door Unlocked"])

def generate_door_unlocked():
    while True:
        yield random.choice([True, False])

def run_dms_simulator(delay, callback, stop_event, name):
    global dms_table
    door_unlocked_generator = generate_door_unlocked()
    for door_unlocked in door_unlocked_generator:
        time.sleep(delay)
        callback(door_unlocked, name, dms_table)
        if stop_event.is_set():
            break