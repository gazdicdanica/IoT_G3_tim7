from flask import Flask
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
import paho.mqtt.publish as publish

app = Flask(__name__)


# InfluxDB Configuration
token = "GLCJTs6_0r7vDXH8QqJ3Yu7kkvvhjgn4fH89E4dl1de38VhXO1ln1cYI13BCTH6-86mPSBF0arD5CRBK6TSG6g=="
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
    publish.single(topic, message, hostname="localhost", port=1883)


def parse_data(data, topic=None):
    if topic == "GDHT":
        send_message("GDHT_Data", parse_gdht(data))
    
    write_to_db(data)


def parse_gdht(data):
    temp_sum = 0
    temp_count = 0
    humidity_sum = 0
    humd_count = 0
    for dht in data["values"]:
        if dht["temperature"] > -40 and dht["temperature"] < 50 and dht["humidity"] > 0 and dht["humidity"] < 100:
            temp_sum += dht["temperature"]
            humidity_sum += dht["humidity"]
            temp_count += 1
            humd_count += 1
    if humd_count == 0:
        humd_count = 1
        temp_count = 1
    return json.dumps({
        "temperature": round(temp_sum/temp_count, 1),
        "humidity": round(humidity_sum/humd_count, 1),
    })


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
