import time
import threading
from sim.pir import run_pir_simulator


def pir_callback(motion_detected, name):
    t = time.localtime()
    print("=" * 20 + ">" + name)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Motion Detected: {motion_detected}")

def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting PIR simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, pir_callback, stop_event, settings['name']))
        pir_thread.start()
        threads.append(pir_thread)
        print("PIR simulator started")
    else:
        from sensors.pir import run_pir_loop, PIR
        print("Starting PIR loop")
        pir = PIR(settings['pin'])
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, pir_callback, stop_event, settings['name']))
        pir_thread.start()
        threads.append(pir_thread)
        print("PIR loop started")