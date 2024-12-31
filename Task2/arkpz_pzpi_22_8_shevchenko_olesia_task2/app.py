from flask import Flask, request
from models import db
from config import Config
from mqtt_handler import start_mqtt_client
from routes.users import users_bp
from routes.labs import labs_bp
from routes.access_events import access_events_bp
from routes.sensors import sensors_bp
from routes.admin_routes import admin_bp
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(labs_bp, url_prefix="/labs")
app.register_blueprint(access_events_bp, url_prefix="/access_events")
app.register_blueprint(sensors_bp, url_prefix="/sensors")
app.register_blueprint(admin_bp, url_prefix="/admin")

@app.route("/")
def home():
    return "API is working!"

if __name__ == "__main__":
    start_mqtt_client()
    app.run(host="0.0.0.0", port=5000)
