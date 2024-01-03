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


def run_4_segment(input_queue, settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting B4SD simulator")
        four_segment_thread = threading.Thread(target=run_4_segment_simulator, args=(input_queue, 60, stop_event, settings['name'], settings['runsOn']))
        four_segment_thread.start()
        threads.append(four_segment_thread)
        print("B4SD simulator started")
    else:
        from actuators.four_segment import run_display_loop,FourSegment
        print("Starting B4SD loop")
        four_segment = FourSegment(settings['name'], settings['segments'], settings['digits'])
        four_thread = threading.Thread(target=run_display_loop, args=(four_segment, stop_event, settings['name'], settings['runsOn']))
        four_thread.start()
        threads.append(four_thread)
        print("B4SD loop started")

