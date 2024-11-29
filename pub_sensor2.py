import time
import json
import random
import paho.mqtt.client as mqtt

# Inisialisasi broker MQTT
broker = "127.0.0.1"
port = 1883

# Inisialisasi topik dan pesan
topic = "home/humidity"

device_info = {
    "device_id": "sensor_livingroom_01",
    "type": "humidity_sensor",
    "location": "living room",
    "topic": topic,
    "unit": "%"
}

client = mqtt.Client()
client.connect(broker, port)
client.loop_start()

client.publish("home/discovery", json.dumps(device_info), retain=True)

try:
    humidity = 50
    while True:
        humidity += random.uniform(-0.5, 0.5)
        sensor_data = {
            "humidity": humidity,
            "unit": "%",
            "timestamp": time.time()
        }
        client.publish(topic, json.dumps(sensor_data))
        print(f"Published: {sensor_data}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Publisher dihentikan.")

finally:
    client.loop_stop()
    client.disconnect()
