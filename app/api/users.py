from app.api import bp
from app.models import User
from flask import jsonify


@bp.route("/users/<int:id>", methods=["GET"])
def getUser(id):
    return jsonify(User.query.get_or_404(id).toDict())
