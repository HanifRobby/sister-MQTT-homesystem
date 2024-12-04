import json
import paho.mqtt.client as mqtt_client
import time

# Ambang batas suhu
TEMPERATURE_THRESHOLD = 35.0

def on_connect(client, userdata, flags, rc):
    print("Aktuator terhubung ke MQTT Broker!")
    # Berlangganan ke topik data sensor yang relevan
    client.subscribe("home/temperature")
    client.subscribe("home/humidity")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        data_type = list(payload.keys())[0]
        value = payload[data_type]
        unit = payload.get('unit', '')
        timestamp = payload.get('timestamp', time.time())

        print(f"Data sensor diterima: {data_type} = {value} {unit} pada {time.ctime(timestamp)}")

        # Mengimplementasikan algoritma untuk berbagai jenis sensor
        if data_type == 'temperature':
            process_temperature(value)
        elif data_type == 'humidity':
            process_humidity(value)
        else:
            print("Jenis data sensor tidak dikenali.")
    except json.JSONDecodeError:
        print("Pesan data sensor tidak valid.")

def process_temperature(value):
    if value >= TEMPERATURE_THRESHOLD:
        activate_alarm()
    else:
        deactivate_alarm()

def process_humidity(value):
    if ((value >= 60) & (value <= 40)):
        activate_alarm()
    else:
        deactivate_alarm()


def activate_alarm():
    # Logika untuk mengaktifkan alarm
    print("Alarm diaktifkan oleh aktuator!")

def deactivate_alarm():
    # Logika untuk menonaktifkan alarm
    print("Alarm dinonaktifkan oleh aktuator.")

# Konfigurasi client MQTT
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message

# Terhubung ke broker
client.connect("127.0.0.1", 1883)
client.loop_forever()