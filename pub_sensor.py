import time
import json
import random
import paho.mqtt.client as mqtt
import ssl

# Inisialisasi broker MQTT
broker = "localhost"
port = 8883

# Path ke sertifikat dan kunci
ca_cert = "/etc/mosquitto/ca_certificates/ca.crt"  # Sertifikat CA
client_cert = "/etc/mosquitto/certs/client.crt"    # Sertifikat klien
client_key = "/etc/mosquitto/certs/client.key"     # Kunci privat klien

# Inisialisasi Client MQTT
client = mqtt.Client()

client.tls_set(
    ca_certs=ca_cert,
    certfile=client_cert,
    keyfile=client_key,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

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