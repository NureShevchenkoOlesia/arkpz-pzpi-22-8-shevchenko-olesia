# IoT-симулятор для генерації даних сенсорів та передачі їх через MQTT

import paho.mqtt.client as mqtt
import json
import random
import time

# Конфігурація MQTT
BROKER = "localhost"
PORT = 1883
TOPIC = "iot/sensor_data"

# Користувачі та лабораторії для генерації даних
USERS = [1, 2, 3, 4]  # ID користувачів
LABS = [1, 2, 3]      # ID лабораторій

# Генерує випадковий вектор для відбитків пальців
def generate_fingerprint():
    return [random.randint(0, 255) for _ in range(128)]  # 128-елементний вектор

# Генерує дані сенсора та відправляє їх через MQTT
def send_sensor_data(client):
    user_id = random.choice(USERS)
    lab_id = random.choice(LABS)
    fingerprint = generate_fingerprint()

    payload = {
        "user_id": user_id,
        "lab_id": lab_id,
        "fingerprint": fingerprint
    }

    try:
        client.publish(TOPIC, json.dumps(payload))
        print(f"Sent data: {payload}")
    except Exception as e:
        print(f"Failed to send data: {e}")

# Запуск симулятора IoT
def start_simulator():
    client = mqtt.Client()

    try:
        client.connect(BROKER, PORT, 60)
        print(f"Connected to MQTT broker at {BROKER}:{PORT}")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return

    client.loop_start()

    try:
        while True:
            send_sensor_data(client)
            time.sleep(5)  # Інтервал передачі даних (у секундах)
    except KeyboardInterrupt:
        print("Simulator stopped by user")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    start_simulator()
