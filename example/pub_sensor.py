import time
import json
import random

import paho.mqtt.client as mqtt

# Inisialisasi broker MQTT
broker = "127.0.0.1"
port = 1883

# Inisialisasi topik dan pesan
topic = "home/temperature"

device_info = {
    "device_id": "sensor_kitchen_02",
    "type": "temperature_sensor",
    "location": "kitchen",
    "topic": topic,
    "unit": "Celsius"
}

client = mqtt.Client()
client.connect(broker, port)
client.loop_start()

client.publish("home/discovery", json.dumps(device_info), retain=True)

try:
    suhu = 30
    while True:
        suhu += random.randint(-2, 2)
        sensor_data = {
            "temperature": suhu,
            "unit": "Celsius",
            "timestamp": time.asctime()
        }
        client.publish(topic, json.dumps(sensor_data))
        print(f"Published: {sensor_data}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Publisher dihentikan.")

finally:
    client.loop_stop()
    client.disconnect()