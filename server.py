from flask import Flask
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)


# InfluxDB Configuration
token = "S6gcEyq18bCgeoFHjR_qKbprW0gOTMIU4gIWSszDJN7TiT4REjbEa4YRfQY9XGhNLWz7yVZxCPlD16-F8rcVyQ=="
org = "iot"
url = "http://localhost:8086"
bucket = "iote"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


def on_connect(client, userdata, flags, rc):
    client.subscribe("RDHT1")
    client.subscribe("RDHT2")
    client.subscribe("RPIR1")
    client.subscribe("RPIR2")
    client.subscribe("DPIR1")
    client.subscribe("DUS1")
    client.subscribe("DS1")
    client.subscribe("DL")
    client.subscribe("DB")
    client.subscribe("DMS")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))


def save_to_db(data):
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
    

@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
