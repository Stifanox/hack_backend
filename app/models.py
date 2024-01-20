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
