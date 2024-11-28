#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:49:00 2024

@author: widhi
"""

import paho.mqtt.client as mqtt

# Callback untuk pesan yang diterima
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")

# Menghubungkan ke broker MQTT
client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)

# Berlangganan ke topik
client.subscribe("sister/temp4")
client.on_message = on_message

# Menjaga koneksi tetap terbuka
client.loop_forever()