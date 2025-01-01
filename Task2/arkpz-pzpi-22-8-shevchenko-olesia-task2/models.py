from flask_sqlalchemy import SQLAlchemy
import bcrypt
from werkzeug.security import check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    access_level = db.Column(db.Integer, nullable=False)
    occupation_id = db.Column(db.Integer, db.ForeignKey("useroccupations.id"))
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "access_level": self.access_level,
            "occupation_id": self.occupation_id
        }

class UserOccupation(db.Model):
    __tablename__ = "useroccupations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(100), nullable=False)

class Lab(db.Model):
    __tablename__ = "labs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    access_requirements = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("labstatuses.id"))

class LabStatus(db.Model):
    __tablename__ = "labstatuses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)

class AccessEvent(db.Model):
    __tablename__ = "accessevents"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"))
    timestamp = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(100), nullable=False, default="pending")
    reason = db.Column(db.String(255))

class Sensor(db.Model):
    __tablename__ = "sensors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"))
    type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    timestamp = db.Column(db.DateTime, default=db.func.now())
    access_data = db.Column(db.String(100), nullable=False) 
    status = db.Column(db.String(50), nullable=False, default='active')
