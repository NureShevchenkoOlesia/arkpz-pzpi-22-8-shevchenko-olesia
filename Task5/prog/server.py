from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
from datetime import datetime

app = Flask(__name__)

REGISTERED_FINGERPRINTS = {
    "user1": "abc123xyz789",
    "user2": "def456uvw123"
}

BROKER = "localhost" 
PORT = 1883  
TOPIC = "sensors/fingerprint"  

def on_message(client, userdata, msg):
    fingerprint = msg.payload.decode()
    print(f"Received fingerprint from MQTT: {fingerprint}")
    
    for user, registered_fingerprint in REGISTERED_FINGERPRINTS.items():
        if fingerprint == registered_fingerprint:
            print(f"Access granted for {user}")
            return

    print("Access denied: Fingerprint not recognized")

def start_mqtt_client():
    client = mqtt.Client("FlaskMQTTServer")
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_start()

@app.route('/')
def index():
    return "Flask Server with MQTT is running!"

if __name__ == "__main__":
    start_mqtt_client()
    app.run(host="0.0.0.0", port=5000)
