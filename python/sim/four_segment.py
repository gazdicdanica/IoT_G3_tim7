import time, datetime

alarm = None
alarm_on = False

def get_time():
    while True:
        current = datetime.datetime.now().replace(second=0)
        yield current.strftime("%H:%M:%S")


def run_4_segment_simulator(alarm_queue, turn_off_queue, delay, stop_event, name, runsOn):
    global alarm, alarm_on 
    time_generator = get_time()
    for t in time_generator:
        if alarm_queue.qsize() > 0:
            a = alarm_queue.get()
            alarm = a
        if turn_off_queue.qsize() > 0:
            alarm_on = False   
        print(f"Current time - {t}")
        print(f"Alarm - {alarm}")
        if alarm is not None and alarm == t:
            # TODO: buzzer
            alarm_on = True
            print("WAKE UP!!")
        
        time.sleep(delay)
        if stop_event.is_set():
            break


   