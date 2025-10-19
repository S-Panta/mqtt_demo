# subscriber and publisher
# rapid sampling and sending alert
import random
import time
import json
import paho.mqtt.client as mqtt_client

subscription_topic = "rainfall"
publish_topic = "waterlevel"
alert_topic = "alerts"

sampling_time = 10
rainfall = 0
rainfall_timestamp = 0

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected:", reason_code)
    client.subscribe(subscription_topic)
    print(f"Subscribed to topic: {subscription_topic}")

def on_message(client, userdata, msg):
    global sampling_time, rainfall,rainfall_timestamp
    data = json.loads(msg.payload.decode())
    rainfall = data.get("rainfall", 0)
    rainfall_timestamp = data.get("timestamp", time.time())
    if rainfall > 20:
        print(f"Alert. The rainfall is {rainfall} mm. Increase data collection frequency.")
        sampling_time = 10
    else:
        sampling_time = 15

def publish_river_guage_data(client):
    global sampling_time, rainfall,rainfall_timestamp

    while True:
        river_level = round(random.uniform(0.1, 5), 2)
        timestamp = time.time()
        river_message = json.dumps({
            "river_level": river_level,
            "timestamp": timestamp,
            "rainfall": rainfall,
            "rainfall_timestamp": rainfall_timestamp
        })
        print(f"Measured river level: {river_level} m in interval of {sampling_time}, rainfall data is {rainfall} mm ")
        client.publish(publish_topic,river_message)

        if river_level > 2.5:
            alert_msg = json.dumps({
                "alert": "FLOOD WARNING",
                "river_level": river_level,
                "timestamp": timestamp
            })
            client.publish(alert_topic, alert_msg)
        time.sleep(sampling_time)

client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost',1883,60)
client.loop_start()
publish_river_guage_data(client)

