from flask import Flask
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
import paho.mqtt.publish as publish

app = Flask(__name__)


# InfluxDB Configuration
token = "PssPnJLkhVs4v7i8wrjq_k_ve58B-4Tmc8IyAwurIZiFktRammEp-AiIBkdAwWXzb-qEevGPqyZycFCw16txCw=="
org = "iot"
url = "http://localhost:8086"
bucket = "iote"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, keepalive=65535)
mqtt_client.loop_start()


g_temp = []
g_humidity = []

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
    # print("Sending message: ", message, topic)
    publish.single(topic, message, hostname="localhost", port=1883)


def parse_data(data, topic=None):
    if topic == "GDHT":
        msg = parse_gdht(data)
        if msg:
            send_message("GDHT_Data", msg)
    
    write_to_db(data)


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
    # print(data)
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
