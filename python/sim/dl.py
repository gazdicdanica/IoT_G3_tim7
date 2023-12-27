import time


light_status = False

def switch_light():
    global light_status
    light_status = not light_status
    

def run_dl_simulator(user_input_queue, delay, callback, stop_event, name, runsOn):
    global light_status
    
    while True:
        if user_input_queue.qsize() > 0:
            user_input = user_input_queue.get()
            if user_input == 'l':
                switch_light()
        callback(light_status, name, True, runsOn)

        if stop_event.is_set():
            break

        time.sleep(delay)
