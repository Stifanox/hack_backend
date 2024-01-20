from app.api import bp
from app.models import User
from flask import jsonify

@bp.route("/users/<int:id>", method=["GET"])
def getUser(id):
    return jsonify(User.query.get_or_404(id).toDict())


@bp.route("/users", method=["POST"])
def addUser():
    pass
