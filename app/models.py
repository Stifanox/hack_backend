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
