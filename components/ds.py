from sim.ds import run_ds_simulator
import threading
import time


def ds_callback(door_opened, name, table):
    time = time.localtime()
    time = time.strftime('%H:%M:%S', time)

    table.add_row([name, time, door_opened])

def run_ds(settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting DS simulator")
        ds_thread = threading.Thread(target=ds_callback, args=())
        ds_thread.start()
        threads.append(ds_thread)
        print("DS simulator started")
    else:
        pass