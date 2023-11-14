from sim.db import run_buzzer_simulator
import threading
import time

def db_callback(buzzer_on, name, table):
    t = time.localtime()
    t = time.strftime('%H:%M:%S', t)

    table.add_row([name, t, buzzer_on])

def run_db(user_input_queue, settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting DB simulator")
        db_thread = threading.Thread(target=run_buzzer_simulator, args=(user_input_queue, 4, db_callback, stop_event, settings['name']))
        db_thread.start()
        threads.append(db_thread)
        print("DB simulator started")
    else:
        from actuators.db import run_db_loop, DoorBuzzer
        print("Starting DB loop")
        db = DoorBuzzer(settings['name'], settings['pin'])
        db_thread = threading.Thread(target=run_db_loop, args=(user_input_queue, db, 2, db_callback, stop_event, settings['name']))
        db_thread.start()
        threads.append(db_thread)
        print("DB loop started")