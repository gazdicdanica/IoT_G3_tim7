import time
import random
from prettytable import PrettyTable

ds_table = PrettyTable(["Sensor", "TimeStamp", "Door Opened"])

def generate_door_opened():
    while True:
        yield random.choice([True, False])

def run_ds_simulator(delay, callback, stop_event, name):
    global ds_table
    door_opened_generator = generate_door_opened()
    for door_opened in door_opened_generator:
        time.sleep(delay)
        callback(door_opened, name, ds_table)
        if stop_event.is_set():
            break