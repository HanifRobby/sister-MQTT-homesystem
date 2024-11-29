import sqlite3
import threading

class Database:
    _instance_lock = threading.Lock()

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.init_db()

    def init_db(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                device_id TEXT,
                data_type TEXT,
                value REAL,
                unit TEXT
            )
        ''')
        self.connection.commit()

    def insert_data(self, timestamp, device_id, data_type, value, unit):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (timestamp, device_id, data_type, value, unit)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, device_id, data_type, value, unit))
        self.connection.commit()

    def fetch_data(self, limit=100):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT timestamp, device_id, data_type, value, unit
            FROM sensor_data
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def get_device_ids(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT DISTINCT device_id FROM sensor_data
        ''')
        rows = cursor.fetchall()
        device_ids = [row[0] for row in rows]
        return device_ids
 
    
    def fetch_data_by_device(self, device_id, limit=100):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT timestamp, device_id, data_type, value, unit
            FROM sensor_data
            WHERE device_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (device_id, limit))
        return cursor.fetchall()

    def close(self):
        self.connection.close()
