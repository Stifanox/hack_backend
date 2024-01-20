from app.api import bp
from app.models import DailyUpdate, User
from flask import jsonify, request
from app import db
import random
import requests
from app.gpt_request_wrapper.GPTMessage import GPTMessage
import ast

@bp.route("/daily-updates", methods=["POST"])
def create_daily_update():
    data = request.json
    if not data:
        return {"error": "No data provided"}, 400

    new_update = DailyUpdate()

    GPTAnswer = requests.post(url="https://api.openai.com/v1/chat/completions",
                             headers={"Authorization": "Bearer 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",
                                      "Content-Type": "application/json"},
                             data=GPTMessage(data["note"]).getMessageForDailyUpdated()
                             )

    isSus = ast.literal_eval(GPTAnswer.json()["choices"][0]["message"]["content"]).get("isSuspicious")

    if isSus == 1:
        new_update.suspicious_message = True
    else:
        new_update.suspicious_message = False

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
    if not uncheered_updates:
        return {"message": "You are banned from sending daily updates"}, 503
    random_update = random.choice(uncheered_updates)
    return jsonify(random_update.toDict())
