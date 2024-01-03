from sim.db import run_buzzer_simulator
import threading, time, json
import paho.mqtt.publish as publish


sensor_data_lock = threading.Lock()
batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
HOSTNAME = ""
PORT = 0


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
    global HOSTNAME, PORT
    HOSTNAME = settings['hostname']
    PORT = settings['port']
    if settings["simulated"]:
        print("Starting DB simulator")
        db_thread = threading.Thread(target=run_buzzer_simulator, args=(user_input_queue, 4, db_callback, stop_event, settings['name'], settings['runsOn']))
        db_thread.start()
        threads.append(db_thread)
        print("DB simulator started")
    else:
        from actuators.db import run_db_loop, DoorBuzzer
        print("Starting DB loop")
        db = DoorBuzzer(settings['name'], settings['pin'])
        db_thread = threading.Thread(target=run_db_loop, args=(user_input_queue, db, 2, db_callback, stop_event, settings['name'], settings['runsOn']))
        db_thread.start()
        threads.append(db_thread)
        print("DB loop started")