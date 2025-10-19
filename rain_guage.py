# only publisher
import random
import time
import json
import paho.mqtt.client as mqtt_client

subscription_topic = "rainfall"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected:", reason_code)

# simulation of site sensor
def publish_rainfall(client):
    while True:
        rainfall = round(random.uniform(10.0, 35.0), 2)
        timestamp = time.time() 
        message = json.dumps({"rainfall": rainfall, "timestamp": timestamp})
        
        result = client.publish(subscription_topic,message)
        status = result[0]
        if status == 0:
            print(f"Rainfall Value {message} mm send to topic `{subscription_topic}`")
        else:
            print("Failed to send message")
        time.sleep(20)

client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect('localhost',1883,60)
client.loop_start()
publish_rainfall(client)

