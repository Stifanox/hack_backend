from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return f'<User {self.username}>'

    def toDict(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "id": self.id
        }

    def fromDict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


class AnonimMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<AnonimMessage {self.id}>'

    def toDict(self):
        return {
            "id": self.id,
            "senderId": self.sender_id,
            "receiverId": self.receiver_id,
            "message": self.message
        }

    def fromDict(self, data):
        if 'senderId' in data:
            self.sender_id = data['senderId']
        if 'receiverId' in data:
            self.receiver_id = data['receiverId']
        if 'message' in data:
            self.message = data['message']


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DailyMood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    short_description = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    mood = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DailyMood {self.id}>'

    def toDict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "shortDescription": self.short_description,
            "description": self.description,
            "mood": self.mood,
            "date": self.date.isoformat() if self.date else None
        }

    def fromDict(self, data):
        if 'userId' in data:
            self.user_id = data['userId']
        if 'shortDescription' in data:
            self.short_description = data['shortDescription']
        if 'description' in data:
            self.description = data['description']
        if 'mood' in data:
            self.mood = data['mood']
        if 'date' in data:
            self.date = datetime.fromisoformat(data['date']) if data['date'] else None
