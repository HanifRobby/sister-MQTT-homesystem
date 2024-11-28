import json
import paho.mqtt.client as mqtt

devices = {}

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
        print(f"Data diterima dari {msg.topic}: {payload}")
        # Tambahkan logika pemrosesan data sensor di sini
    except json.JSONDecodeError:
        print(f"Data diterima dari {msg.topic}: {msg.payload.decode()} (format tidak valid)")


# Konfigurasi client MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Menambahkan callback untuk topik discovery
client.message_callback_add("home/discovery", on_discovery_message)

# Menambahkan callback untuk topik data sensor
client.on_message = on_sensor_data  # Default callback untuk topik lain

# Terhubung ke broker
client.connect("127.0.0.1", 1883)
client.loop_forever()

