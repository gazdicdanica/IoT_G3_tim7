import threading
import time
from scripts.load_settings import load_settings
from components.dht11 import run_dht
from components.pir import run_pir
from components.dl import run_dl
from components.hcsr04 import run_ultrasonic
from components.ds import run_ds
from components.dms import run_dms
from components.db import run_db
import sim.dht11 as dht_data
import sim.pir as pir_data
import sim.hcsr04 as hcsr_data
import sim.ds as ds_data
import sim.dms as dms_data
import sim.dl as dl_data
import sim.db as db_data
from prettytable import PrettyTable
from queue import Queue


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

concatenated_table = PrettyTable(["Sensor", "Timestamp", "Humidity", "Temperature", "Code", "Motion Detected", "Distance"])
door_table = PrettyTable([ "Door Unlocked", "Door Opened"])

light_queue = Queue()
buzzer_queue = Queue()

def concat_tables(table1, table2, table3):
    max_rows = max(len(table1._rows), len(table2._rows), len(table3._rows))

    for table in [table1, table2, table3]:
        while len(table._rows) < max_rows:
            table.add_row([""] * len(table.field_names))

    concatenated_table = PrettyTable()

    for field_name in table1.field_names + table2.field_names + table3.field_names:
        concatenated_table.add_column(field_name, [])

    for row1, row2, row3 in zip(table1._rows, table2._rows, table3._rows):
        concatenated_table.add_row(row1 + row2 + row3)

    return concatenated_table

def door_tables(table1, table2, table3, table4):
    max_rows = max(len(table1._rows), len(table2._rows), len(table3._rows), len(table4._rows))

    for table in [table1, table2, table3, table4]:
        while len(table._rows) < max_rows:
            table.add_row([""] * len(table.field_names))

    door_table = PrettyTable()

    for field_name in table1.field_names +  table2.field_names + table3.field_names + table4.field_names:
        door_table.add_column(field_name, [])

    for row1, row2, row3, row4 in zip(table1._rows, table2._rows, table3._rows, table4._rows):
        door_table.add_row(row1 + row2 + row3 + row4)

    return door_table

def run_user_input_threads(threads, stop_event):
    input_thread = threading.Thread(target=user_input_thread, args=(stop_event,))
    input_thread.start()
    threads.append(input_thread)

def user_input_thread(stop_event):
    global light_queue
    global buzzer_queue

    while True:
        user_input = input()
        if user_input == 'l':
            light_queue.put(user_input)
        if user_input == 'b':
            buzzer_queue.put(user_input)
        time.sleep(0.1)
        if stop_event.is_set():
            break

if __name__ == "__main__":
    print("*** G3 Tim7 ***")
    threads = []
    stop_event = threading.Event()
    pi1_settings = load_settings("1")

    try:
        dht1_settings = pi1_settings['RDHT1']
        dht2_settings = pi1_settings['RDHT2']
        rpir1_settings = pi1_settings['RPIR1']
        rpir2_settings = pi1_settings['RPIR2']
        dpir1_settings = pi1_settings['DPIR1']
        dus1_settings = pi1_settings['DUS1']
        ds1_settings = pi1_settings['DS1']
        dms_settings = pi1_settings['DMS']
        dl_settings = pi1_settings['DL']
        db_settings = pi1_settings['DB']

        run_user_input_threads(threads, stop_event)

        run_dht(dht1_settings, threads, stop_event)
        run_dht(dht2_settings, threads, stop_event)

        run_pir(rpir1_settings, threads, stop_event)
        run_pir(rpir2_settings, threads, stop_event)
        run_pir(dpir1_settings, threads, stop_event)

        run_ds(ds1_settings, threads, stop_event)
        run_dms(dms_settings, threads, stop_event)
        run_dl(light_queue, dl_settings, threads, stop_event)
        run_db(buzzer_queue, db_settings, threads, stop_event)

        run_ultrasonic(dus1_settings, threads, stop_event)

        while True:
            time.sleep(4)

            concatenated_table = concat_tables(pir_data.pir_table, dht_data.dht_table, hcsr_data.ultrasonic_table)
            door_table = door_tables(ds_data.ds_table, dms_data.dms_table, dl_data.dl_table, db_data.db_table)
            print(concatenated_table)
            print(door_table)

            pir_data.pir_table.clear_rows()
            dht_data.dht_table.clear_rows()
            hcsr_data.ultrasonic_table.clear_rows()
            dms_data.dms_table.clear_rows()
            ds_data.ds_table.clear_rows()
            dl_data.dl_table.clear_rows()
            db_data.db_table.clear_rows()


    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()