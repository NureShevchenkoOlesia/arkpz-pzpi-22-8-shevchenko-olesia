# Маршрути для роботи з сенсорами

from flask import Blueprint, request, jsonify
from models import db, Sensor
import datetime

# Ініціалізація Blueprint
sensors_bp = Blueprint("sensors", __name__)

REGISTERED_FINGERPRINTS = {
    "user1": "abc123xyz789",
    "user2": "def456uvw123"
}

# Отримати список усіх сенсорів
@sensors_bp.route("/", methods=["GET"])
def get_sensors():
    try:
        sensors = Sensor.query.all()
        sensors_list = [
            {
                "id": sensor.id,
                "lab_id": sensor.lab_id,
                "user_id": sensor.user_id,
                "access_data": sensor.access_data,
                "last_verified": sensor.timestamp,
            }
            for sensor in sensors
        ]
        return jsonify(sensors_list), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch sensors", "details": str(e)}), 500

# Створити новий сенсор
@sensors_bp.route("/", methods=["POST"])
def create_sensor():
    try:
        data = request.json
        sensor = Sensor(
            lab_id=data["lab_id"],
            user_id=data["user_id"],
            type=data["type"],
            access_data=data["access_data"],
        )
        db.session.add(sensor)
        db.session.commit()
        return jsonify({"message": "Sensor created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": "Failed to create sensor", "details": str(e)}), 500

# Видалити сенсор за ID
@sensors_bp.route("/<int:sensor_id>", methods=["DELETE"])
def delete_sensor(sensor_id):
    try:
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return jsonify({"error": "Sensor not found"}), 404

        db.session.delete(sensor)
        db.session.commit()
        return jsonify({"message": "Sensor deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete sensor", "details": str(e)}), 500

@sensors_bp.route("/fingerprint", methods=["POST"])
def verify_fingerprint():
    data = request.json
    fingerprint = data.get("access_data")
    if not fingerprint:
        return jsonify({"error": "No fingerprint data provided"}), 400
    for user, registered_fingerprint in REGISTERED_FINGERPRINTS.items():
        if fingerprint == registered_fingerprint:
            return jsonify({"status": "approved", "user": user, "timestamp": datetime.now()}), 200
    return jsonify({"status": "denied", "reason": "Fingerprint not recognized"}), 403



