from datetime import datetime
from sqlalchemy import BOOLEAN
from app import db
import time


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    general_streak = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

    def toDict(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "id": self.id,
            "generalStreak": self.general_streak
        }

    def fromDict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


class DailyUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    note = db.Column(db.Text)
    is_cheered = db.Column(db.Boolean, default=False)
    timestamp_new = db.Column(db.BigInteger, index=True, default=round(time.time() * 1000))
    suspicious_message = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<DailyUpdate {self.id}>'

    def toGPTDict(self):
        return {
            "id": self.id,
            "note": self.note
        }

    def toDict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "rating": self.rating,
            "note": self.note,
            "isCheered": self.is_cheered,
            "timestamp": self.timestamp_new,
            "suspiciousMessage": self.suspicious_message
        }

    def fromDict(self, data):
        if 'userId' in data:
            self.user_id = data['userId']
        if 'rating' in data:
            self.rating = data['rating']
        if 'note' in data:
            self.note = data['note']
        if 'isCheered' in data:
            self.is_cheered = data['isCheered']


class Cheerup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    update_id = db.Column(db.Integer, db.ForeignKey('daily_update.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp_new = db.Column(db.BigInteger, index=True, default=round(time.time() * 1000))

    def __repr__(self):
        return f'<Cheerup {self.id}>'

    def toDict(self):
        return {
            "id": self.id,
            "updateId": self.update_id,
            "receiverId": self.receiver_id,
            "senderId": self.sender_id,
            "content": self.content,
            "timestamp": self.timestamp_new
        }

    def fromDict(self, data):
        if 'updateId' in data:
            self.update_id = data['updateId']
        if 'receiverId' in data:
            self.receiver_id = data['receiverId']
        if 'senderId' in data:
            self.sender_id = data['senderId']
        if 'content' in data:
            self.content = data['content']


class Habits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    habit_id = db.Column(db.Integer)
    timestamp_new = db.Column(db.BigInteger, default=round(time.time() * 1000))
    timestamp_broken_new = db.Column(db.BigInteger)
    broken = db.Column(BOOLEAN, default=False)
    updated_at = db.Column(db.BigInteger)

    def toDict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "habitId": self.habit_id,
            "timestamp": self.timestamp_new,
            "broken": self.broken,
            "timestampBroken": self.timestamp_broken_new,
            "updatedAt": self.updated_at
        }

    def updateTimestamp(self):
        self.updated_at = round(time.time() * 1000)


class BadMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def toDict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'message': self.message
        }


class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    page = db.Column(db.String(100))
    is_accepted = db.Column(db.Boolean, default=True, name='is_accepted')
    description = db.Column(db.Text)

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'page': self.page,
            'isAccepted': self.is_accepted,
            'description': self.description
        }

    def fromDict(self, data):
        for field in ['name', 'email', 'phone', 'page', 'isAccepted', 'description']:
            if field in data:
                if field == 'isAccepted':
                    setattr(self, 'is_accepted', data[field])
                else:
                    setattr(self, field, data[field])
