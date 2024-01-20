from app.api import bp


@bp.route("/users/<int:id>", method=["GET"])
def getUser(id):
    pass


@bp.route("/users", method=["POST"])
def addUser():
    pass
