from flask import Blueprint, jsonify, request
from admin_utils import backup_database, export_data_to_json, import_data_from_json
from reports import generate_access_report
from decorators import admin_required

admin_bp = Blueprint("admin", __name__)

# Резервне копіювання бази даних
@admin_bp.route("/backup", methods=["POST"])
@admin_required
def backup():
    file_path = backup_database()
    return jsonify({"message": "Backup created successfully!", "file": file_path}), 200

# Експортує дані системи в JSON-файл
@admin_bp.route("/export", methods=["GET"])
@admin_required
def export_data():
    file_path = export_data_to_json()
    return jsonify({"message": "Data exported successfully!", "file": file_path}), 200

# Генерує звіт про події доступу
@admin_bp.route("/report", methods=["GET"])
@admin_required
def generate_report():
    file_path = generate_access_report()
    return jsonify({"message": "Report generated successfully!", "file": file_path}), 200
