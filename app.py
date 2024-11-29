from flask import Flask, render_template, jsonify, request
import os
import sys

# Menambahkan path ke modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from database import Database

app = Flask(__name__)

# Inisialisasi database
db_path = os.path.join(os.path.dirname(__file__), 'database', 'sensor_data.db')
db = Database(db_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices')
def devices():
    # Mendapatkan daftar device_id unik dari database
    devices_ids = db.get_devices_ids()
    return jsonify(devices_ids)

@app.route('/data')
def data():
    # Mengambil parameter device_id
    device_id = request.args.get('device_id')

    # Mengambil data terbaru untuk device_id tertentu
    if device_id:
        sensor_data = db.fetch_data_by_device(device_id, 100)
    else:
        sensor_data = db.fetch_data(100)
    data_list = []
    for data_point in sensor_data:
        timestamp, device_id, data_type, value, unit = data_point
        data_list.append({
            'timestamp': timestamp,
            'device_id': device_id,
            'data_type': data_type,
            'value': value,
            'unit': unit
        })
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
