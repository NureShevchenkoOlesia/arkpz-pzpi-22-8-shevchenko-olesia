import os
from datetime import datetime
import json
from models import db, User, Lab, AccessEvent

# Створення резервної копії бази даних
def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"
    os.system(f"pg_dump lab_access_control > backups/{backup_file}")
    return backup_file

# Експортує дані з бази до JSON-файлу
def export_data_to_json():
    data = {
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "access_level": user.access_level,
                "occupation_id": user.occupation_id
            }
            for user in User.query.all()
        ],
        "labs": [
            {
                "id": lab.id,
                "title": lab.title,
                "access_requirements": lab.access_requirements,
                "status_id": lab.status_id
            }
            for lab in Lab.query.all()
        ],
        "access_events": [
            {
                "id": event.id,
                "user_id": event.user_id,
                "lab_id": event.lab_id,
                "timestamp": str(event.timestamp),
                "status": event.status,
                "reason": event.reason
            }
            for event in AccessEvent.query.all()
        ],
    }

    with open("exports/system_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    return "exports/system_data.json"

# Імпортує дані з JSON-файлу в базу
def import_data_from_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Імпорт користувачів
        for user_data in data.get("users", []):
            user = User(**user_data)
            db.session.add(user)

        # Імпорт лабораторій
        for lab_data in data.get("labs", []):
            lab = Lab(**lab_data)
            db.session.add(lab)

        # Імпорт подій доступу
        for event_data in data.get("access_events", []):
            event_data["timestamp"] = datetime.strptime(event_data["timestamp"], "%Y-%m-%d %H:%M:%S")
            event = AccessEvent(**event_data)
            db.session.add(event)

        db.session.commit()
        return "Data imported successfully!"
    except Exception as e:
        db.session.rollback()
        return f"Error importing data: {e}"

