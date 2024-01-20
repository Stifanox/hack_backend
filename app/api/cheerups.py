from app.api import bp
from flask import jsonify, request
from app import db
from app.models import Cheerup, DailyUpdate


@bp.route("/cheerups", methods=["POST"])
def create_cheerup():
    data = request.json

    daily_update = DailyUpdate.query.get(data.get("updateId"))
    if daily_update.is_cheered:
        return jsonify({"error": "This DailyUpdate has already been cheered"}), 418,

    new_cheerup = Cheerup()
    new_cheerup.fromDict(data)

    daily_update = DailyUpdate.query.get(new_cheerup.update_id)
    daily_update.is_cheered = True

    db.session.add(new_cheerup)
    db.session.commit()
    return jsonify(new_cheerup.toDict()), 201


@bp.route("/cheerups/update/<int:update_id>", methods=["GET"])
def get_cheerup_by_update(update_id):
    cheerup = Cheerup.query.filter_by(update_id=update_id).first()
    return jsonify(cheerup.toDict())


@bp.route("/cheerups/user/<int:user_id>", methods=["GET"])
def get_cheerups_by_user(user_id):
    cheerups = Cheerup.query.filter_by(receiver_id=user_id).all()
    return jsonify([cheerup.toDict() for cheerup in cheerups])
