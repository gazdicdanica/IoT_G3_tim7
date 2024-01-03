from sim.dms import run_dms_simulator
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
            print(f'published dms values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dms_callback(door_unlocked, name, simulated, runsOn):
    global sensor_data_lock, publish_data_counter, publish_data_limit
    t = time.localtime()
    t = time.strftime('%H:%M:%S', t)
    data = {
        "measurement": name,
        "name": name,
        "simulated": simulated,
        "runsOn": runsOn,
        "values": {
            "door_unlocked": 1.0 if door_unlocked else 0.0
        },
        "code": 200,
        "timestamp": t
    }
    with counter_lock:
        batch.append((name, json.dumps(data), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dms(settings, threads, stop_event):
    global HOSTNAME, PORT
    HOSTNAME = settings['hostname']
    PORT = settings['port']
    if settings["simulated"]:
        print("Starting DMS simulator")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(4, dms_callback, stop_event, settings['name'], settings['runsOn']))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS simulator started")
    else:
        from sensors.dms import run_dms_loop, DMS
        print("Starting DMS loop")
        dms = DMS(settings['name'], settings['pins'])
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, 2, dms_callback, stop_event, settings['name'], settings['runsOn']))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS loop started")