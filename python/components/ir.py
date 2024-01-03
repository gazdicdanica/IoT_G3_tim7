import time, threading, json

def run_ir(settings, threads, stop_event):
    if settings['simulated']:
        pass
    else:
        from sensors.ir import run_ir_loop, IR
        print("Starting IR loop")
        ir = IR(settings['name'], settings['pin'])
        ir_thread = threading.Thread(target=run_ir_loop, args=(ir, 2, stop_event, settings['name'], settings['runsOn']))
        ir_thread.start()
        threads.append(ir_thread)
        print("IR loop started")