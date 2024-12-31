# Модуль для обробки MQTT-повідомлень

import paho.mqtt.client as mqtt
import json
from models import db, Sensor
from datetime import datetime

# Конфігурація MQTT
BROKER = "localhost"
PORT = 1883
TOPIC = "iot/sensor_data"

# Функція викликається при підключенні до брокера
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT connected successfully")
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect to MQTT broker. Return code: {rc}")

# Функція обробляє вхідні повідомлення з топіка
def on_message(client, userdata, msg):
    try:
        # Розбір повідомлення
        payload = json.loads(msg.payload.decode("utf-8"))
        user_id = payload["user_id"]
        lab_id = payload["lab_id"]
        fingerprint = payload["fingerprint"]

        # Пошук відповідного сенсора в базі
        sensor = Sensor.query.filter_by(user_id=user_id, lab_id=lab_id).first()
        if not sensor:
            print(f"Sensor not found for user {user_id} in lab {lab_id}")
            return

        # Порівняння векторів відбитків
        if fingerprint != json.loads(sensor.fingerprint_data):
            print(f"Fingerprint mismatch for user {user_id}")
            return

        # Оновлення часу перевірки сенсора
        sensor.last_verified = datetime.utcnow()
        db.session.commit()
        print(f"Sensor verified successfully for user {user_id} in lab {lab_id}")

    except json.JSONDecodeError:
        print("Invalid JSON received")
    except Exception as e:
        print(f"Error processing message: {e}")

# Запуск MQTT-клієнта
def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, 60)
        print(f"Connected to MQTT broker at {BROKER}:{PORT}")
        client.loop_start()
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
