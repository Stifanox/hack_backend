from app.api import bp
from app.models import User
from flask import jsonify
from flask import request
from app.common.response import SuccessLogin, ErrorLogin, ErrorRegister, SuccessRegister
from app import db


@bp.route("/users/<int:id>", methods=["GET"])
def getUser(id):
    return jsonify(User.query.get_or_404(id).toDict())


@bp.route("/login", methods=["POST"])
def loginUser():
    if "user" not in request.json or "password" not in request.json:
        return ErrorLogin("There are no required fields ('user', 'password')").__dict__

    user = User.query.filter_by(username=request.json["user"]).first()

    if not user:
        return ErrorLogin("Invalid username or password").__dict__

    if user.password == request.json["password"]:
        return SuccessLogin({"user": request.json["user"]}).__dict__
    else:
        return ErrorLogin("Invalid username or password").__dict__


@bp.route("/register", methods=["POST"])
def registerUser():
    if "user" not in request.json or "password" not in request.json:
        return ErrorRegister("There are no required fields ('user', 'password')").__dict__

    checkUser = User.query.filter_by(username=request.json["user"]).first()

    if checkUser:
        return ErrorRegister("User exists").__dict__

    newUser = User(username=request.json["user"], password=request.json["password"])
    db.session.add(newUser)
    db.session.commit()

    return SuccessRegister("Dodano uzytkownka").__dict__
