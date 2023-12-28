import time, threading, json
from sim.four_segment import run_4_segment_simulator
import paho.mqtt.publish as publish

sensor_data_lock = threading.Lock()
batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
HOSTNAME = ""
PORT = 0

# def publisher_task(event, _batch):


def run_4_segment(settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting 4D7S Display simulator")
        four_segment_thread = threading.Thread(target=run_4_segment_simulator, args=(60, stop_event, settings['name'], settings['runsOn']))
        four_segment_thread.start()
        threads.append(four_segment_thread)
        print("4D7S Display simulator started")
    else:
        from actuators.four_segment import FourSegment
        print("Starting 4D7S Display loop")
        four_segment = FourSegment(settings['name'], settings['segments'], settings['digits'])
        four_thread = threading.Thread(target=four_segment.show_time)
        four_thread.start()
        threads.append(four_thread)
        print("4D7S Display loop started")

