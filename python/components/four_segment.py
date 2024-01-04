import datetime, threading, json
from queue import Queue
from sim.four_segment import run_4_segment_simulator
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt


sensor_data_lock = threading.Lock()
batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
HOSTNAME = ""
PORT = 0
mqtt_client = mqtt.Client()

alarm_time = Queue()
turn_off = Queue()

# def publisher_task(event, _batch):

def on_connect(client, userdata, flags, rc):
    print("B4SD connected")
    client.subscribe("wake_up_data")

def on_message(client, userdata, msg):
    global alarm_time
    data = json.loads(msg.payload.decode('utf-8'))
    print(data)
    if not bool(data["turn_off"]):
        alarm_time.put(datetime.datetime.strptime(data["alarm_time"], "%H:%M:%S").time())
    else:
        turn_off.put(True)



def run_4_segment(settings, threads, stop_event):
    global HOSTNAME, PORT, alarm_time, turn_off, mqtt_client
    HOSTNAME = settings['hostname']
    PORT = settings['port']
    mqtt_client.connect(HOSTNAME, PORT, keepalive=65535)
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    if settings["simulated"]:
        print("Starting B4SD simulator")
        four_segment_thread = threading.Thread(target=run_4_segment_simulator, args=(alarm_time, turn_off, 60, stop_event, settings['name'], settings['runsOn']))
        four_segment_thread.start()
        threads.append(four_segment_thread)
        print("B4SD simulator started")
    else:
        from actuators.four_segment import run_display_loop,FourSegment
        print("Starting B4SD loop")
        four_segment = FourSegment(settings['name'], settings['segments'], settings['digits'])
        four_thread = threading.Thread(target=run_display_loop, args=(alarm_time, turn_off, four_segment, stop_event, settings['name'], settings['runsOn']))
        four_thread.start()
        threads.append(four_thread)
        print("B4SD loop started")

