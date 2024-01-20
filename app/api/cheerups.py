import ast

from app.api import bp
from flask import jsonify, request
from app import db
from app.models import Cheerup, DailyUpdate, BadMessage, User
import requests
from app.gpt_request_wrapper.GPTMessage import GPTMessage
from app.common.response import success, failed


@bp.route("/cheerups", methods=["POST"])
def create_cheerup():
    data = request.json

    print(data["content"])
    GPTAnswer = requests.post(url="https://api.openai.com/v1/chat/completions",
                              headers={"Authorization": "Bearer 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",
                                       "Content-Type": "application/json"},
                              data=GPTMessage(data["content"]).getCheerMessage()
                              )

    if ast.literal_eval(GPTAnswer.json()["choices"][0]["message"]["content"]).get("value") == 1:
        new_bad_message = BadMessage(user_id=data["senderId"], message=data["content"])
        db.session.add(new_bad_message)
        db.session.commit()
        if BadMessage.query.filter_by(user_id=data['senderId']).count() >= 3:
            User.query.filter_by(id=data['senderId']).first().banned = 1
            db.session.commit()
            return failed(f"Nie można wysłać wiadomości o treści: {data['content']}. Wysyłanie cheersów zostaje zablokowane."), 418
        return failed(f"Nie można wysłać wiadomości o treści: {data['content']}"), 418

    daily_update = DailyUpdate.query.get(data.get("updateId"))
    if daily_update.is_cheered:
        return jsonify({"error": "This DailyUpdate has already been cheered"}), 418,

    new_cheerup = Cheerup()
    new_cheerup.fromDict(data)

    daily_update = DailyUpdate.query.get(new_cheerup.update_id)
    daily_update.is_cheered = True

    print(data["senderId"])
    userWhoCheered = User.query.filter_by(id=int(data["senderId"])).first()
    userWhoCheered.general_streak = userWhoCheered.general_streak + 1

    db.session.add(new_cheerup)
    db.session.commit()
    return success(new_cheerup.toDict()), 201


@bp.route("/cheerups/update/<int:update_id>", methods=["GET"])
def get_cheerup_by_update(update_id):
    cheerup = Cheerup.query.filter_by(update_id=update_id).first()
    return jsonify(cheerup.toDict())


@bp.route("/cheerups/user/<int:user_id>", methods=["GET"])
def get_cheerups_by_user(user_id):
    cheerups = Cheerup.query.filter_by(receiver_id=user_id).all()
    return jsonify([cheerup.toDict() for cheerup in cheerups])
