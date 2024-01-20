from flask import request

from app import app, db
from app.common.response import success, failed


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        user_props = {name: request.json[name] for name in request.json if name not in {'password'}}
        newuser = User(**user_props)
        newuser.set_password(request.json['password'])
        db.session.add(newuser)
        db.session.commit()
        return success(newuser.to_dict())
    elif request.method == 'GET':
        try:
            users = User.query.all()
            # return success([simple_user.to_dict() for simple_user in users])
        except Exception as e:
            return failed(str(e))


@app.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_simple(user_id):
    if request.method == 'GET':
        try:
            user = User.query.get(user_id)
            return success(user.to_dict())
        except:
            return failed("Nie znaleziono użytkownika")
    if request.method == 'PUT':
        print("body")
        print(request.json)
        User.query.filter_by(id=user_id).update(dict(request.json))

        db.session.commit()

        user = User.query.get(user_id)
        print(user.to_dict())
        return success(user.to_dict())
    if request.method == 'DELETE':
        try:
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()

            return success({"id": user_id})
        except:
            return failed("Usuwanie użytkownika nie powiodło się")
