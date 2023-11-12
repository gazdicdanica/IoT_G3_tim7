import threading
import time
from scripts.load_settings import load_settings
from components.dht11 import run_dht
from components.pir import run_pir
import sim.dht11 as dht_data
import sim.pir as pir_data
import sim.hcsr04 as hcsr_data
import sim.ds as ds_data
import sim.dms as dms_data
from components.hcsr04 import run_ultrasonic
from components.ds import run_ds
from components.dms import run_dms
from prettytable import PrettyTable


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

concatenated_table = PrettyTable(["Sensor", "Timestamp", "Humidity", "Temperature", "Code", "Motion Detected", "Distance"])
door_table = PrettyTable([ "Door Unlocked", "Door Opened"])

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

def door_tables(table1, table2):
    max_rows = max(len(table1._rows), len(table2._rows))

    for table in [table1, table2]:
        while len(table._rows) < max_rows:
            table.add_row([""] * len(table.field_names))

    door_table = PrettyTable()

    for field_name in table1.field_names + table2.field_names:
        door_table.add_column(field_name, [])

    for row1, row2 in zip(table1._rows, table2._rows):
        door_table.add_row(row1 + row2)

    return door_table

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
        dms1_settings = pi1_settings['DMS']

        run_dht(dht1_settings, threads, stop_event)
        run_dht(dht2_settings, threads, stop_event)

        run_pir(rpir1_settings, threads, stop_event)
        run_pir(rpir2_settings, threads, stop_event)
        run_pir(dpir1_settings, threads, stop_event)

        run_ds(ds1_settings, threads, stop_event)
        run_dms(dms1_settings, threads, stop_event)

        run_ultrasonic(dus1_settings, threads, stop_event)

        while True:
            time.sleep(5)

            concatenated_table = concat_tables(pir_data.pir_table, dht_data.dht_table, hcsr_data.ultrasonic_table)
            door_table = door_tables(ds_data.ds_table, dms_data.dms_table)
            print(concatenated_table)
            print(door_table)

            pir_data.pir_table.clear_rows()
            dht_data.dht_table.clear_rows()
            hcsr_data.ultrasonic_table.clear_rows()
            dms_data.dms_table.clear_rows()
            ds_data.ds_table.clear_rows()


    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()