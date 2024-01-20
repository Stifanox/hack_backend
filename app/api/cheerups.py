from app.api import bp
from flask import jsonify, request
from app import db
from app.models import Cheerup, DailyUpdate
import requests
from app.gpt_request_wrapper.GPTMessage import GPTMessage

@bp.route("/cheerups", methods=["POST"])
def create_cheerup():
    data = request.json

    daily_update = DailyUpdate.query.get(data.get("updateId"))
    if daily_update.is_cheered:
        return jsonify({"error": "This DailyUpdate has already been cheered"}), 418,

    new_cheerup = Cheerup()
    new_cheerup.fromDict(data)

    GPTAnswer = requests.post(url="https://api.openai.com/v1/chat/completions",
                              headers={"Authorization":"Bearer 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",
                                       "Content-Type":"application/json"},
                              data= GPTMessage(data["content"]).getMessage()
                              )
    print(GPTAnswer.json())
    print(GPTAnswer.json()["choices"][0]["message"]["content"])

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
