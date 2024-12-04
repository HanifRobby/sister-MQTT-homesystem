import json
import paho.mqtt.client as mqtt_client
import time

def on_connect(client, userdata, flags, rc):
    print("Aktuator terhubung ke MQTT Broker!")
    # Berlangganan ke topik perintah
    client.subscribe("home/commands/alarm")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        command = payload.get('command')
        value = payload.get('value')
        timestamp = payload.get('timestamp', time.time())

        print(f"Perintah diterima: {command} = {value} pada {time.ctime(timestamp)}")

        # Melakukan aksi berdasarkan perintah
        if command == 'alarm':
            if value == 'ON':
                activate_alarm()
            elif value == 'OFF':
                deactivate_alarm()
            else:
                print("Nilai perintah tidak dikenal.")
        else:
            print("Jenis perintah tidak dikenal.")
    except json.JSONDecodeError:
        print("Pesan perintah tidak valid.")

def activate_alarm():
    # Logika untuk mengaktifkan alarm
    print("Alarm diaktifkan!")

def deactivate_alarm():
    # Logika untuk menonaktifkan alarm
    print("Alarm dinonaktifkan.")

# Konfigurasi client MQTT
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message

# Terhubung ke broker
client.connect("127.0.0.1", 1883)
client.loop_forever()
