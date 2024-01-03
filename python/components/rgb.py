from sim.rgb import run_rgb_simulator
import threading, time, json

def run_rgb(user_input_queue, settings, threads, stop_event):
    if settings['simulated']:
        print('Starting RGB simulator')
        rgb_thread = threading.Thread(target=run_rgb_simulator, args=(user_input_queue, 5, stop_event, settings['name'], settings['runsOn']))
        rgb_thread.start()
        threads.append(rgb_thread)
        print("RGB simulator started")
    else:
        from actuators.rgb import run_rgb_loop, RGB
        print("Starting RGB loop")
        rgb = RGB(settings['name'], settings["R_pin"], settings["G_pin"], settings["B_pin"])
        rgb_thread = threading.Thread(target=run_rgb_loop, args=(user_input_queue, rgb, 5, stop_event, settings['name'], settings['runsOn']))
        rgb_thread.start()
        threads.append(rgb_thread)
        print("RGB loop started")