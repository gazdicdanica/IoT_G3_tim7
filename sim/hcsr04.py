import time
import random
from prettytable import PrettyTable


ultrasonic_table = PrettyTable(["Sensor", "Timestamp", "Distance"])


def generate_distance():
    distance = 100  # Starting distance
    while True:
        distance += random.randint(-5, 5)  # Simulate fluctuations
        if distance < 0:
            distance = 0
        yield distance

def run_ultrasonic_simulator(delay, callback, stop_event, name):
    global ultrasonic_table
    distance_generator = generate_distance()
    for distance in distance_generator:
        time.sleep(delay)
        callback(distance, name, ultrasonic_table)
        if stop_event.is_set():
            break
