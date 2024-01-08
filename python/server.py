from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json, time, threading
import paho.mqtt.publish as publish
import datetime

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@socketio.on('subscribe')
def handle_subscribe(topic):
    join_room(topic)
    print(f"Subscribed to {topic}")


# InfluxDB Configuration
token = "b2Rw7AZug6z8VHqJX2wH1A19oxM1eyvnxzly0rwabSAlJ6TkHDRIjNVZyXZr902RnQog9Ed3hphzXAaXZjNltw=="
org = "iot"
url = "http://localhost:8086"
bucket = "iote"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883)
mqtt_client.loop_start()

ALARM_TRIGGERED = False
SYSTEM_ACTIVATED = True

g_temp = []
g_humidity = []
dht_treshold = 10

dpir1_motion_data = []
dpir1_treshold_percentage = 50
dpir1_motion_data_len_treshold = 10

ds_readings = []
ds_readings_len_treshold = 10
ds_threshold_percentage = 50


def send_ws_message(topic, message):
    socketio.emit('message', message, room=topic)


def send_message(topic, message):
    print("Sending message: ", message, topic)
    publish.single(topic, message, hostname="localhost", port=1883)

def send_alarm():
    global ALARM_TRIGGERED
    send_message("ALARM", json.dumps({"alarm": 1 if ALARM_TRIGGERED else 0}))
    time.sleep(10)


activation_thread = threading.Thread(target=send_alarm)
activation_thread.start()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("RDHT1")
    client.subscribe("RDHT2")
    client.subscribe("RDHT3")
    client.subscribe("RDHT4")
    client.subscribe("GDHT")

    client.subscribe("RPIR1")
    client.subscribe("RPIR2")
    client.subscribe("RPIR3")
    client.subscribe("RPIR4")
    client.subscribe("DPIR1")
    client.subscribe("DPIR2")
    
    client.subscribe("DUS1")
    client.subscribe("DUS2")

    client.subscribe("DS1")
    client.subscribe("DS2")
    client.subscribe("DL")
    client.subscribe("DB")
    client.subscribe("BB")
    client.subscribe("DMS")
    send_message("DMS_Data", json.dumps({"triggered": ALARM_TRIGGERED, "activated": SYSTEM_ACTIVATED}))

    client.subscribe("GSG")
    client.subscribe("ALERT")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    topic = msg.topic
    print("TOPIC")
    print(topic)
    parse_data(data, topic)


def parse_data(data, topic=None):
    global ALARM_TRIGGERED, SYSTEM_ACTIVATED


    if topic == "ALERT":
        trigger_alarm(data['name'], data["runsOn"], data["simulated"])
        ALARM_TRIGGERED = True

    elif SYSTEM_ACTIVATED:
        if topic == "GDHT":
            msg = parse_gdht(data)
            if msg:
                send_message("GDHT_Data", msg)
            write_to_db(data)
        elif topic == "DPIR1":
            if parse_pir(data):
                send_message("DL_Data", json.dumps({"motion_detected": 1}))
            write_to_db(data)
        elif topic == "DS1" or topic == "DS2":
            if parse_ds(data):
                if not ALARM_TRIGGERED:
                    trigger_alarm(topic, data["runsOn"], data["simulated"])
                    ALARM_TRIGGERED = True
            else:
                ALARM_TRIGGERED = False
        elif topic == "DMS":
            parse_dms(data)
        elif topic == "B4SD":
            parse_b4sd(data)
        else:
            write_to_db(data)
    elif topic == "DMS":
        parse_dms(data)


def parse_b4sd(data):
    print(data)
    if isinstance(data, str):
        data = json.loads(data)
    values = data.get('values', {})
    alarm = values.get('alarm', 0)
    if alarm is True:
        send_ws_message("wake_up", json.dumps(data))
    else:
        send_ws_message("time", values.get('time', 0))

def parse_dms(data):
    global ALARM_TRIGGERED, SYSTEM_ACTIVATED
    try:
        if isinstance(data, str):
            data = json.loads(data)
        values = data.get('values', {})
        action = values.get('action', 0)
        print(action, ALARM_TRIGGERED, SYSTEM_ACTIVATED)
        if action == 1:
            print(ALARM_TRIGGERED, SYSTEM_ACTIVATED)
            if SYSTEM_ACTIVATED:
                SYSTEM_ACTIVATED = False
            elif ALARM_TRIGGERED:
                ALARM_TRIGGERED = False
            elif not SYSTEM_ACTIVATED:
                SYSTEM_ACTIVATED = True
        else:
            print("Wrong pin")
            trigger_alarm(data['name'], data["runsOn"], data["simulated"])
            return
        send_message("DMS_Data", json.dumps({"triggered": ALARM_TRIGGERED, "activated": SYSTEM_ACTIVATED}))
        write_to_db(data)
    except:
        print("Error decoding JSON data")


def parse_ds(data):
    global ds_readings, ds_readings_len_treshold
    try:
        if isinstance(data, str):
            data = json.loads(data)
        values = data.get('values', {})
        door_opened = values.get('door_opened', 0)
        ds_readings.append(door_opened)
    except:
        print("Error decoding JSON data")
    # print(ds_readings)
    if len(ds_readings) >= ds_readings_len_treshold:
        truthy_count = ds_readings.count(1)
        total_count = len(ds_readings)
        percentage_truthy = (truthy_count / total_count) * 100
        ds_readings = []
        return percentage_truthy >= ds_threshold_percentage

def parse_pir(data):
    global dpir1_motion_data, dpir1_treshold_percentage, dpir1_motion_data_len_treshold
    try:
        if isinstance(data, str):
            data = json.loads(data)
        values = data.get('values', {})
        motion_detected = values.get('motion_detected', 0)
        dpir1_motion_data.append(motion_detected)
    except:
        print("Error decoding JSON data")
    # print(dpir1_motion_data)
    if len(dpir1_motion_data) >= dpir1_motion_data_len_treshold:
        truthy_count = dpir1_motion_data.count(1)
        total_count = len(dpir1_motion_data)
        percentage_truthy = (truthy_count / total_count) * 100
        dpir1_motion_data = []
        return percentage_truthy >= dpir1_treshold_percentage
    

def parse_gdht(data):
    global g_temp, g_humidity, dht_treshold
    try:
        if isinstance(data, str):
            data = json.loads(data)
        values = data.get('values', {})

        temperature = values.get('temperature', 0)
        humidity = values.get('humidity', 0)
        if -20 < temperature < 50 and 0 < humidity < 100:
            g_temp.append(temperature)
            g_humidity.append(humidity)
    except:
        print("Error decoding JSON data")
        return json.dumps({"temperature": 0, "humidity": 0})
    if len(g_temp) >= dht_treshold:
        average_temperature = round(sum(g_temp) / len(g_temp),1)
        average_humidity = round(sum(g_humidity) / len(g_humidity),1)
        g_temp = []
        g_humidity = []
        return json.dumps({"temperature": average_temperature, "humidity": average_humidity})


def trigger_alarm(trigger, pi, simulated):
    send_message("ALARM", json.dumps({"alarm": 1}))
    
    t = time.strftime('%H:%M:%S', time.localtime())
    data = {
        "measurement": "ALARM",
        "name": "ALARM",
        "trigger": trigger,
        "simulated": simulated,
        "runsOn": pi,
        "values": {
            "alarm": 1
        },
        "code": 200,
        "timestamp": t
    }
    write_to_db(data)


def write_to_db(data):
    print(data)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("name", data["name"])
        .tag("simulated", data["simulated"])
        .tag('runsOn', data["runsOn"])
        .tag('code', data["code"])
    )
    for field_name, field_value in data["values"].items():
        point.field(field_name, field_value)
    point.field("timestamp", data["timestamp"])

    write_api.write(bucket=bucket, org=org, record=point)
    

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def to_time(date_string): 
    try:
        return datetime.datetime.strptime(date_string, "%H:%M").time()
    except ValueError:
        raise ValueError('{} is not valid time in the format HH:mm'.format(date_string))



@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/api/set_wakeup_time', methods=['GET'])
def set_wakeup_time():
    try:
        time = to_time(request.args.get('time'))
        print(f"Setting wakeup time to {time}")
        send_message("wake_up_data", json.dumps({"alarm_time": str(time), "turn_off": str(False)}))
        return jsonify({}), 200
    except ValueError as ex:
        return jsonify({'error': str(ex)}), 400 
    
@app.route('/api/turn_off_alarm', methods=['GET'])
def turn_off_alarm():
    try:
        send_message("wake_up_data", json.dumps({"alarm_time": "", "turn_off": str(True)}))
        return jsonify({}), 200
    except ValueError as ex:
        return jsonify({'error': str(ex)}), 400


if __name__ == '__main__':
    app.run()
