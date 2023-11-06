

from sim.dht11 import run_dht_simulator
import threading
import time

def dht_callback(humidity, temperature, code, name):
    t = time.localtime()
    print("="*20+">"+ name)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dht1 sumulator")
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event, settings['name']))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 sumulator started")
        else:
            from sensors.dht11 import run_dht_loop, DHT
            print("Starting dht1 loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, settings['name']))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 loop started")
