from sim.ds import run_ds_simulator
import threading
import time


def ds_callback(door_opened, name, table):
    t = time.localtime()
    t = time.strftime('%H:%M:%S', t)

    table.add_row([name, t, door_opened])

def run_ds(settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting DS simulator")
        ds_thread = threading.Thread(target=run_ds_simulator, args=(4, ds_callback, stop_event, settings['name']))
        ds_thread.start()
        threads.append(ds_thread)
        print("DS simulator started")
    else:
        pass