from sim.dms import run_dms_simulator
import threading
import time


def dms_callback(door_unlocked, name, table):
    time = time.localtime()
    time = time.strftime('%H:%M:%S', time)

    table.add_row([name, time, door_unlocked])

def run_ds(settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting DMS simulator")
        dms_thread = threading.Thread(target=dms_callback, args=())
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS simulator started")
    else:
        pass