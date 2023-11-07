from sim.hcsr04 import run_ultrasonic_simulator  # Import the ultrasonic simulator
import threading
import time

def ultrasonic_callback(distance, name):
    t = time.localtime()
    print("=" * 20 + ">" + name)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Distance: {distance} cm")

def run_ultrasonic(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting Ultrasonic simulator")
        ultrasonic_thread = threading.Thread(target=run_ultrasonic_simulator, args=(2, ultrasonic_callback, stop_event, settings['name']))
        ultrasonic_thread.start()
        threads.append(ultrasonic_thread)
        print("Ultrasonic simulator started")
    else:
        from sensors.hcsr04 import run_ultrasonic_loop, UltrasonicSensor
        print("Starting Ultrasonic loop")
        ultrasonic = UltrasonicSensor(settings['echo_pin'], settings['trigger_pin'])
        ultrasonic_thread = threading.Thread(target=run_ultrasonic_loop, args=(ultrasonic, 2, ultrasonic_callback, stop_event, settings['name']))
        ultrasonic_thread.start()
        threads.append(ultrasonic_thread)
        print("Ultrasonic loop started")
