from sim.dms import run_dms_simulator
import threading
import time


def dms_callback(door_unlocked, name, table):
    t = time.localtime()
    t = time.strftime('%H:%M:%S', t)

    table.add_row([name, t, door_unlocked])

def run_dms(settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting DMS simulator")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(4, dms_callback, stop_event, settings['name']))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS simulator started")
    else:
        pass