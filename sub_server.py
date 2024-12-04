import json
import paho.mqtt.client as mqtt_client
import ssl
import time
import os
import sys

# Menambahkan path ke modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from database import Database

# Inisialisasi database
db_path = os.path.join(os.path.dirname(__file__), 'database', 'sensor_data.db')
db = Database(db_path)

devices = {}
client = mqtt_client.Client()

# Path ke sertifikat dan kunci
ca_cert = "/etc/mosquitto/ca_certificates/ca.crt"  # Sertifikat CA
client_cert = "/etc/mosquitto/certs/client.crt"    # Sertifikat klien
client_key = "/etc/mosquitto/certs/client.key"     # Kunci privat klien

# Mengatur TLS dengan sertifikat klien
client.tls_set(
    ca_certs=ca_cert,
    certfile=client_cert,
    keyfile=client_key,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

def on_connect (client, userdata, flags, rc):
    print("Connected to MQTT Broker!")
    client.subscribe("home/discovery")

def on_discovery_message(client, userdata, msg):
    print("Pesan dari dicovery masuk")
    try:
        # Parsing payload JSON
        payload = json.loads(msg.payload.decode())
        device_id = payload["device_id"]
        device_topic = payload["topic"]

        # Menambahkan perangkat baru ke daftar perangkat
        if device_id not in devices:
            devices[device_id] = payload
            print(f"Perangkat baru ditemukan: {payload}")

            # Subscribe secara otomatis ke topik perangkat baru
            client.subscribe(device_topic)
            print(f"Berlangganan ke topik: {device_topic}")
        else:
            print(f"Perangkat {device_id} sudah terdaftar.")

    except json.JSONDecodeError:
        print("Gagal memproses pesan discovery. Pastikan format JSON valid.")

def on_sensor_data(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        data_type = list (payload.keys())[0]
        value = payload[data_type]
        unit = payload.get('unit', '')
        timestamp = payload.get('timestamp', time.time())
        device_id = None

        # Mencari device_id berdasarkan topik
        for device in devices.values():
            if device['topic'] == msg.topic:
                device_id = device['device_id']
                break

        if device_id is None:
            print(f"Device ID tidak ditemukan untuk topik {msg.topic}")
            return

        print(f"Data diterima dari {device_id}: {data_type} = {value} {unit}")

        # Menyimpan data ke database
        db.insert_data(timestamp, device_id, data_type, value, unit)


    except json.JSONDecodeError:
        print(f"Data diterima dari {msg.topic}: {msg.payload.decode()} (format tidak valid)")


# Konfigurasi client MQTT
client.on_connect = on_connect

# Menambahkan callback untuk topik discovery
client.message_callback_add("home/discovery", on_discovery_message)

# Menambahkan callback untuk topik data sensor
client.on_message = on_sensor_data

# Terhubung ke broker
client.connect("127.0.0.1", 8883)
client.loop_forever()

