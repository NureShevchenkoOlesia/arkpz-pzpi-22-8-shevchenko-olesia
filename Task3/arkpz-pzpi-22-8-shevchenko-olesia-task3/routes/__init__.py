from flask import Blueprint
from routes.users import users_bp
from routes.labs import labs_bp
from routes.access_events import access_events_bp
from routes.sensors import sensors_bp

__all__ = ["users_bp", "labs_bp", "access_events_bp", "sensors_bp"]
