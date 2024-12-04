import time
import json
import random

import paho.mqtt.client as mqtt

# Inisialisasi broker MQTT
broker = "127.0.0.1"
port = 8883

# Path ke sertifikat dan kunci
ca_cert = "/path/to/ca.crt"            # Sertifikat CA
client_cert = "/path/to/client.crt"    # Sertifikat klien
client_key = "/path/to/client.key"     # Kunci privat klien

# Inisialisasi Client MQTT
client = mqtt.Client()

# Inisialisasi topik dan pesan
topic = "home/temperature"

device_info = {
    "device_id": "sensor_kitchen_01",
    "type": "temperature_sensor",
    "location": "kitchen",
    "topic": topic,
    "unit": "Celsius"
}

# Terhubung ke broker
client.connect(broker, port)
client.loop_start()

client.publish("home/discovery", json.dumps(device_info), retain=True)

try:
    suhu = 30
    while True:
        suhu += random.uniform(-0.5, 0.5)
        sensor_data = {
            "temperature": suhu,
            "unit": "Celsius",
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