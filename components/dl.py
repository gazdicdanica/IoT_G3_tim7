from sim.dl import run_dl_simulator
import threading
import time

def dl_callback(light_on, name, table):
    t = time.localtime()
    t = time.strftime('%H:%M:%S', t)

    table.add_row([name, t, light_on])

def run_dl(user_input_queue, settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting DL simulator")
        dl_thread = threading.Thread(target=run_dl_simulator, args=(user_input_queue, 4, dl_callback, stop_event, settings['name']))
        dl_thread.start()
        threads.append(dl_thread)
        print("DL simulator started")
    else:
        from actuators.dl import run_dl_loop, DL
        print("Starting DL loop")
        dl = DL(settings['name'], settings['pin'])
        dl_thread = threading.Thread(target=run_dl_loop, args=(user_input_queue, dl, 2, dl_callback, stop_event, settings['name']))
        dl_thread.start()
        threads.append(dl_thread)
        print("DL loop started")