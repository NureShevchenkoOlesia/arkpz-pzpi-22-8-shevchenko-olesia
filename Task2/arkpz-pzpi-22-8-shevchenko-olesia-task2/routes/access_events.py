# Маршрути для роботи з подіями доступу

from flask import Blueprint, request, jsonify, session
from models import db, AccessEvent, Lab, User, Sensor
from datetime import datetime 

# Ініціалізація Blueprint
access_events_bp = Blueprint("access_events", __name__)

# Отримати всі події доступу 
@access_events_bp.route("/", methods=["GET"])
def get_access_events():
    try:
        events = AccessEvent.query.all()
        events_list = [
            {
                "id": event.id,
                "user_id": event.user_id,
                "lab_id": event.lab_id,
                "timestamp": event.timestamp,
                "status": event.status,
                "reason": event.reason,
            }
            for event in events
        ]
        return jsonify(events_list), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch access events", "details": str(e)}), 500

# Події доступу користувача
@access_events_bp.route("/me", methods=["GET"])
def get_user_access_events():
    user_id = session.get("user_id")
    access_events = AccessEvent.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": event.id, "lab_id": event.lab_id, "timestamp": event.timestamp, "status": event.status, "reason": event.reason
    } for event in access_events]), 200

def _log_access_event(user_id, lab_id, status, reason):
    access_event = AccessEvent(
        user_id=user_id,
        lab_id=lab_id,
        timestamp=datetime.datetime.now(),
        status=status,
        reason=reason
    )
    db.session.add(access_event)
    db.session.commit()
    return jsonify({
        "message": reason,
        "status": status
    }), 201 if status == "approved" else 403

def check_biometrics(sensor, user):
    return True

# Створити запит після перевірки даних
@access_events_bp.route("/", methods=["POST"])
def create_access_event():
    try:
        data = request.json
        user_id = session.get("user_id")
        lab_id = data["lab_id"]

        # Перевірка існування лабораторії
        lab = Lab.query.get(lab_id)
        if not lab:
            return jsonify({"error": "Lab not found"}), 404

        # Перевірка рівня доступу
        user = User.query.get(user_id)
        if user.access_level < lab.access_requirements:
            return jsonify({"error": "Access level too low"}), 403

        # Перевірка статусу лабораторії
        if lab.status_id != 0:  # 0 означає "вільна"
            return jsonify({"error": "Lab is not available"}), 403

        # Перевірка біометричних даних через сенсор
        sensor = Sensor.query.filter_by(lab_id=lab_id, user_id=user_id).first()
        if not sensor:
            reason = "Biometric sensor data not found"
            status = "denied"
        else:
            reason = None
            status = "approved"

        # Створення події доступу
        event = AccessEvent(
            user_id=user_id,
            lab_id=lab_id,
            timestamp=datetime.utcnow(),
            status=status,
            reason=reason,
        )
        db.session.add(event)
        db.session.commit()

        return jsonify({"message": "Access event created", "event": {
            "id": event.id,
            "user_id": event.user_id,
            "lab_id": event.lab_id,
            "timestamp": event.timestamp,
            "status": event.status,
            "reason": event.reason,
        }}), 201
    except Exception as e:
        return jsonify({"error": "Failed to create access event", "details": str(e)}), 500


