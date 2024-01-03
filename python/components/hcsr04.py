from sim.hcsr04 import run_ultrasonic_simulator  # Import the ultrasonic simulator
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
            # print(local_batch)
            print(f'published hcsr values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch,))
publisher_thread.daemon = True
publisher_thread.start()


def ultrasonic_callback(distance, name, simulated, runsOn):
    global sensor_data_lock, publish_data_counter, publish_data_limit

    t = time.localtime()
    t = time.strftime('%H:%M:%S', t)
    data = {
        "measurement": name,
        "name": name,
        "simulated": simulated,
        "runsOn": runsOn,
        "values": {
            "distance": distance,
        },
        "code": 200,
        "timestamp": t,
    }
    with counter_lock:
        batch.append((name, json.dumps(data), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_ultrasonic(settings, threads, stop_event):
    global HOSTNAME, PORT
    HOSTNAME = settings['hostname']
    PORT = settings['port']
    if settings['simulated']:
        print("Starting Ultrasonic simulator")
        ultrasonic_thread = threading.Thread(target=run_ultrasonic_simulator, args=(2.5, ultrasonic_callback, stop_event, settings['name'], settings['runsOn']))
        ultrasonic_thread.start()
        threads.append(ultrasonic_thread)
        print("Ultrasonic simulator started")
    else:
        from sensors.hcsr04 import run_ultrasonic_loop, UltrasonicSensor
        print("Starting Ultrasonic loop")
        ultrasonic = UltrasonicSensor(settings['echo_pin'], settings['trigger_pin'])
        ultrasonic_thread = threading.Thread(target=run_ultrasonic_loop, args=(ultrasonic, 2, ultrasonic_callback, stop_event, settings['name'], settings['runsOn']))
        ultrasonic_thread.start()
        threads.append(ultrasonic_thread)
        print("Ultrasonic loop started")
