# Маршрути для роботи з лабораторіями

from flask import Blueprint, request, jsonify
from models import db, Lab, LabStatus

# Ініціалізація Blueprint
labs_bp = Blueprint("labs", __name__)

# Отримати список усіх лабораторій
@labs_bp.route("/", methods=["GET"])
def get_labs():
    try:
        labs = Lab.query.all()
        labs_list = [
            {
                "id": lab.id,
                "title": lab.title,
                "access_requirements": lab.access_requirements,
                "status_id": lab.status_id,
            }
            for lab in labs
        ]
        return jsonify(labs_list), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch labs", "details": str(e)}), 500

# Додати нову лабораторію
@labs_bp.route("/", methods=["POST"])
def create_lab():
    try:
        data = request.json
        lab = Lab(
            title=data["title"],
            access_requirements=data["access_requirements"],
            status_id=data["status_id"],
        )
        db.session.add(lab)
        db.session.commit()
        return jsonify({"message": "Lab created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": "Failed to create lab", "details": str(e)}), 500

# Оновити дані лабораторії за ID
@labs_bp.route("/<int:lab_id>", methods=["PUT"])
def update_lab(lab_id):
    try:
        lab = Lab.query.get(lab_id)
        if not lab:
            return jsonify({"error": "Lab not found"}), 404

        data = request.json
        lab.title = data.get("title", lab.title)
        lab.access_requirements = data.get("access_requirements", lab.access_requirements)
        lab.status_id = data.get("status_id", lab.status_id)
        db.session.commit()
        return jsonify({"message": "Lab updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update lab", "details": str(e)}), 500

# Змінити статус лабораторії
@labs_bp.route("/<int:lab_id>/update_status", methods=["PATCH"])
def update_lab_status(lab_id):
    data = request.json
    lab = Lab.query.get_or_404(lab_id)
    new_status = LabStatus.query.get(data["status_id"])
    if not new_status:
        return jsonify({"error": "Invalid status_id"}), 400
    lab.status_id = data["status_id"]
    db.session.commit()
    return jsonify({"message": f"Lab status updated to {new_status.type}!"})

# Видалити лабораторію за ID
@labs_bp.route("/<int:lab_id>", methods=["DELETE"])
def delete_lab(lab_id):
    try:
        lab = Lab.query.get(lab_id)
        if not lab:
            return jsonify({"error": "Lab not found"}), 404

        db.session.delete(lab)
        db.session.commit()
        return jsonify({"message": "Lab deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete lab", "details": str(e)}), 500
