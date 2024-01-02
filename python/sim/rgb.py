import time

def run_rgb_simulator(input_queue, delay, stop_event, name, runsOn):
    while True:
        if input_queue.qsize() > 0:
            user_input = input_queue.get()
            if user_input == "x":
                print("RGB - off")
                pass
            elif user_input == "w":
                print("RGB - white")
                pass
            elif user_input == "r":
                print("RGB - red")
                pass
            elif user_input == "g":
                print("RGB - green")
                pass
            elif user_input == "b":
                print("RGB - blue")
                pass
            elif user_input == "y":
                print("RGB - yellow")
                pass
            elif user_input == "p":
                print("RGB - purple")
                pass
            elif user_input == "lb":
                print("RGB - light blue")
                pass
        if stop_event.is_set():
            break

        time.sleep(delay)