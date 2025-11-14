import paho.mqtt.client as mqtt_client
publisher_topic = "Environment Temperature"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected:", reason_code)
    client.subscribe(publisher_topic)
    print(f"Subscribed to topic: {publisher_topic}")

def on_message(client, userdata, msg):
    temperature = float(msg.payload.decode())
    if temperature > 20:
        print(f"Alert. The temperature is {temperature}. Take the data.")


client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost',1883,60)
client.loop_forever()