import time, datetime

alarm = None
alarm_on = False

def get_time():
    while True:
        current = datetime.datetime.now()
        yield current.strftime("%H:%M")


def run_4_segment_simulator(alarm_queue, turn_off_queue, delay, stop_event, name, runsOn):
    global alarm, alarm_on
    if alarm_queue.qsize() > 0:
        a = alarm_queue.get()
        alarm = a
    if turn_off_queue.qsize() > 0:
        alarm_on = False    


    time_generator = get_time()
    for t in time_generator:
        print(f"Current time - {t}")
        if alarm == t:
            # TODO: buzzer
            alarm_on = True
            print("WAKE UP!!")
        
        time.sleep(delay)
        if stop_event.is_set():
            break


   