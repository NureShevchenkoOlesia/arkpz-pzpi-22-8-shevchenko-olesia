# Декоратори для перевірки авторизації та адміністративних прав

from functools import wraps
from flask import session, jsonify
from models import User

# Перевіряє, чи авторизований користувач
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Перевіряє, чи користувач має адміністративні права (occupation_id = 6)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        user = User.query.get(user_id)
        if not user or user.occupation_id != 6:
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(*args, **kwargs)
    return decorated_function
