import ast

import requests

from app.api import bp
from app.gpt_request_wrapper.GPTMessage import GPTMessage
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


@bp.route("/daily-updates/matcher/<int:userId>", methods=["GET"])
def get_random_uncheered(userId):
    uncheered_updates = DailyUpdate.query.filter_by(is_cheered=False).filter(
        DailyUpdate.rating < 3, DailyUpdate.user_id != 1).all()
    if not uncheered_updates:
        return {"message": "No uncheered updates available"}, 404
    random_update = random.choice(uncheered_updates)

    try:
        user_updates = DailyUpdate.query.filter_by(user_id=userId).filter(DailyUpdate.rating < 3).all()

        GPTAnswer = requests.post(url="https://api.openai.com/v1/chat/completions",
                                  headers={
                                      "Authorization": "Bearer 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",
                                      "Content-Type": "application/json"},
                                  data=GPTMessage(
                                      ", ".join(
                                          [f"{user_update.id}. {user_update.note}" for user_update in user_updates]))
                                  .getDailyUpdateMessage(
                                      ", ".join(
                                          [f"{uncheered_update.id}. {uncheered_update.note}" for uncheered_update in
                                           uncheered_updates]))
                                  )

        print(ast.literal_eval(GPTAnswer.json()["choices"][0]["message"]["content"]).get("id"))

        id = ast.literal_eval(GPTAnswer.json()["choices"][0]["message"]["content"]).get("id")
        return jsonify(DailyUpdate.query.filter_by(id=id).first().toDict())
    except:
        return jsonify(random_update.toDict())
