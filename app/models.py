from datetime import datetime

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


class DailyUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    note = db.Column(db.Text)
    is_cheered = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<DailyUpdate {self.id}>'

    def toDict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "rating": self.rating,
            "note": self.note,
            "isCheered": self.is_cheered,
            "timestamp": self.timestamp.isoformat()
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
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Cheerup {self.id}>'

    def toDict(self):
        return {
            "id": self.id,
            "update_id": self.update_id,
            "receiver_id": self.receiver_id,
            "sender_id": self.sender_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

    def fromDict(self, data):
        for field in ['update_id', 'receiver_id', 'sender_id', 'content']:
            if field in data:
                setattr(self, field, data[field])
