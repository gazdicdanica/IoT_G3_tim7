import time

def get_time():
    while True:
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        yield f"{current_hour}:{current_minute}"


def run_4_segment_simulator(input_queue, delay, stop_event, name, runsOn):
    #TODO: budilnik 

    time_generator = get_time()
    for t in time_generator:
        print(f"Current time - {t}")
        time.sleep(delay)
        if stop_event.is_set():
            break


   