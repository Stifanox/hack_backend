import json

from app.api import bp
from app.models import User
from flask import jsonify
from flask import request
from app.common.response import SuccessLogin, ErrorLogin
from app import db


@bp.route("/users/<int:id>", methods=["GET"])
def getUser(id):
    return jsonify(User.query.get_or_404(id).toDict())


@bp.route("/login", methods=["POST"])
def loginUser():
    fields = ["user", "password"]
    if not all(name in fields for name in request.form):
        return ErrorLogin("There are no required fields ('user', 'password')").__dict__

    user = User.query.filter_by(username=request.form["user"]).first()

    if not user:
        return ErrorLogin("Invalid username or password").__dict__

    if user.password == request.form["password"]:
        return SuccessLogin(json.dumps({"user": request.form["user"]})).__dict__
    else:
        return ErrorLogin("Invalid username or password").__dict__


@bp.route("/register", methods=["POST"])
def registerUser():
    fields = ["user", "password"]
    if not all(name in fields for name in request.form):
        return ErrorLogin("There are no required fields ('user', 'password')").__dict__

    newUser = User(username=request.form["user"], password=request.form["password"])
    db.session.add(newUser)
    db.session.commit()
    return "Dodano uzytkownika"
