# Маршрути для роботи з користувачами

from flask import Blueprint, request, jsonify, session
from models import db, User
from decorators import login_required, admin_required
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

# Ініціалізація Blueprint
users_bp = Blueprint("users", __name__)

# Отримати список усіх користувачів 
@users_bp.route("/", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        users_list = [
            {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "access_level": user.access_level,
                "occupation_id": user.occupation_id,
            }
            for user in users
        ]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500

# Створення нового користувача 
@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.json
        hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
        user = User(
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            password=hashed_password,  # Хешований пароль
            access_level=data["access_level"],
            occupation_id=data["occupation_id"],
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500

# Оновити дані користувача за ID
@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        data = request.json
        user.name = data.get("name", user.name)
        user.surname = data.get("surname", user.surname)
        user.email = data.get("email", user.email)
        if "password" in data:
            user.password = generate_password_hash(data["password"], method="pbkdf2:sha256")
        db.session.commit()
        return jsonify({"message": "User updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update user", "details": str(e)}), 500

# Видалити користувача за ID 
@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"})

# Авторизація користувача
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
    session["user_id"] = user.id
    session["access_level"] = user.access_level
    return jsonify({"message": "Logged in successfully", "user": user.to_dict()}), 200

@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out successfully!"}), 200
