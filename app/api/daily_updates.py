from app.api import bp
from app.models import DailyUpdate, User
from flask import jsonify, request
from app import db
import random


@bp.route("/daily-updates", methods=["POST"])
def create_daily_update():
    data = request.json
    if not data:
        return {"error": "No data provided"}, 400

    new_update = DailyUpdate()
    new_update.fromDict(data)
    db.session.add(new_update)
    db.session.commit()
    return jsonify(new_update.toDict()), 201


@bp.route("/daily-updates/user/<int:user_id>", methods=["GET"])
def get_daily_updates(user_id):
    updates = DailyUpdate.query.filter_by(user_id=user_id).all()
    return jsonify([update.toDict() for update in updates])


@bp.route("/daily-updates/user", methods=["GET"])
def get_random_uncheered():
    uncheered_updates = DailyUpdate.query.filter_by(is_cheered=False).filter(DailyUpdate.rating < 3).all()
    if not uncheered_updates:
        return {"message": "No uncheered updates available"}, 404
    random_update = random.choice(uncheered_updates)
    return jsonify(random_update.toDict())
