from flask import Flask
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
import paho.mqtt.publish as publish

app = Flask(__name__)


# InfluxDB Configuration
token = "cE7Ju58CY7uIwggkfIfQUp2-sc5W_4OmyVdpbR4EMAqWmo0MlxnPCL9ucxUjieP3074fNm6N3vtRSipaefWm4Q=="
org = "iot"
url = "http://localhost:8086"
bucket = "iote"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883)
mqtt_client.loop_start()


g_temp = []
g_humidity = []
dpir1_motion_data = []
dpir1_treshold_percentage = 50

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

    client.subscribe("GSG")
    client.subscribe("GYRO_ALERT")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    topic = msg.topic
    parse_data(data, topic)


def send_message(topic, message):
    print("Sending message: ", message, topic)
    publish.single(topic, message, hostname="localhost", port=1883)


def parse_data(data, topic=None):
    if topic == "GDHT":
        msg = parse_gdht(data)
        if msg:
            send_message("GDHT_Data", msg)
    elif topic == "DPIR1":
        if parse_pir(data):
            send_message("DL_Data", json.dumps({"motion_detected": 1}))

    write_to_db(data)


def parse_pir(data):
    global dpir1_motion_data, dpir1_treshold_percentage
    try:
        if isinstance(data, str):
            data = json.loads(data)
        values = data.get('values', {})
        motion_detected = values.get('motion_detected', 0)
        dpir1_motion_data.append(motion_detected)
    except:
        print("Error decoding JSON data")
    print(dpir1_motion_data)
    if len(dpir1_motion_data) >= 10:
        truthy_count = dpir1_motion_data.count(1)
        total_count = len(dpir1_motion_data)
        percentage_truthy = (truthy_count / total_count) * 100
        dpir1_motion_data = []
        return percentage_truthy >= dpir1_treshold_percentage
    

def parse_gdht(data):
    global g_temp, g_humidity
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
    if len(g_temp) >= 10:
        average_temperature = round(sum(g_temp) / len(g_temp),1)
        average_humidity = round(sum(g_humidity) / len(g_humidity),1)
        g_temp = []
        g_humidity = []
        return json.dumps({"temperature": average_temperature, "humidity": average_humidity})



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


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
