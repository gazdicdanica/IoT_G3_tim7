from sim.db import run_buzzer_simulator
import threading, time, json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from queue import Queue


sensor_data_lock = threading.Lock()
batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
HOSTNAME = ""
PORT = 0
should_turn_on_bb = Queue()
should_turn_on_db = Queue()
wake_up_bb = Queue()
mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Buzzer connected")
    client.subscribe("ALARM")


def on_message(client, userdata, msg):
    global should_turn_on
    data = json.loads(msg.payload.decode('utf-8'))
    print(data)
    if not data["wake_up"]:
        should_turn_on_db.put(data["alarm"] == 1)    
    should_turn_on_bb.put(data["alarm"] == 1)


def publisher_task(event, _batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_batch = _batch.copy()
            publish_data_counter = 0
            _batch.clear()
            publish.multiple(local_batch, hostname=HOSTNAME, port=PORT)
            print(f'published db values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch,))
publisher_thread.daemon = True
publisher_thread.start()


def db_callback(buzzer_on, name, simulated, runsOn):
    global sensor_data_lock, publish_data_counter, publish_data_limit
    t = time.localtime()
    t = time.strftime('%H:%M:%S', t)
    data = {
        "measurement": name,
        "name": name,
        "simulated": simulated,
        "runsOn": runsOn,
        "values": {
            "buzzer_on": 1.0 if buzzer_on else 0.0
        },
        "code": 200,
        "timestamp": t
    }
    with counter_lock:
        batch.append((name, json.dumps(data), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_db(user_input_queue, settings, threads, stop_event):
    global HOSTNAME, PORT, should_turn_on_bb, should_turn_on_db, mqtt_client
    HOSTNAME = settings['hostname']
    PORT = settings['port']
    mqtt_client.connect(HOSTNAME, PORT, keepalive=65535)
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    if settings["simulated"]:
        db_thread = threading.Thread(target=run_buzzer_simulator, args=(should_turn_on_db, should_turn_on_bb, user_input_queue, 4, db_callback, stop_event, settings['name'], settings['runsOn']))
        db_thread.start()
        threads.append(db_thread)
    else:
        from actuators.db import run_db_loop, DoorBuzzer
        print("Starting DB loop")
        db = DoorBuzzer(settings['name'], settings['pin'])
        db_thread = threading.Thread(target=run_db_loop, args=(should_turn_on_db, should_turn_on_bb, user_input_queue, db, 2, db_callback, stop_event, settings['name'], settings['runsOn']))
        db_thread.start()
        threads.append(db_thread)
        print("DB loop started")