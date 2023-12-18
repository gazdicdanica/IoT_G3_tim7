import time

buzzer_status = False

def switch_buzzer():
    global buzzer_status
    buzzer_status = not buzzer_status

def run_buzzer_simulator(user_input_queue, delay, callback, stop_event, name, runsOn):
    global buzzer_status

    while True:
        if user_input_queue.qsize() > 0:
            user_input = user_input_queue.get()
            if user_input == 'b':
                switch_buzzer()
        callback(buzzer_status, name, True, runsOn)

        if stop_event.is_set():
            break

        time.sleep(delay)
