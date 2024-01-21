import ast

import requests
from sqlalchemy import func

from app.api import bp
from app.gpt_request_wrapper.GPTMessage import GPTMessage
from app.models import DailyUpdate, User, Therapist, Habits, Cheerup
from flask import jsonify, request
from app import db, app
import random
import requests
from app.gpt_request_wrapper.GPTMessage import GPTMessage
import ast
from app.api.gpt_api_key import GPT_API_KEY


@bp.route('/therapist', methods=['POST'])
def create_therapist():
    data = request.json
    therapist = Therapist()
    therapist.fromDict(data)
    db.session.add(therapist)
    db.session.commit()
    return jsonify(therapist.toDict()), 201


@app.route('/therapists', methods=['GET'])
def get_all_therapists():
    therapists = Therapist.query.all()
    return jsonify([therapist.toDict() for therapist in therapists]), 200


@app.route('/therapist/<int:id>', methods=['GET'])
def get_therapist(id):
    therapist = Therapist.query.get_or_404(id)
    return jsonify(therapist.toDict()), 200


@app.route('/therapists/filtered/<int:userId>', methods=['GET'])
def get_filtered_therapists(userId):
    therapists = [f"{therapist.id}. {therapist.name} - {therapist.description}\n" for therapist in
                  Therapist.query.all()]

    all_messages = ", ".join([cheerup.content for cheerup in Cheerup.query.filter_by(sender_id=userId).all()]).join(
        [update.note for update in DailyUpdate.query.filter_by(user_id=userId).all()])

    try:
        GPTAnswer = requests.post(url="https://api.openai.com/v1/chat/completions",
                                  headers={
                                      "Authorization": f"Bearer {GPT_API_KEY}",
                                      "Content-Type": "application/json"},
                                  data=GPTMessage(all_messages).getRecommendedTherapistList(therapists)
                                  )

        therapistIds = ast.literal_eval(GPTAnswer.json()["choices"][0]["message"]["content"]).get("ids")
        return [therapist.toDict() for therapist in Therapist.query.filter(Therapist.id.in_(therapistIds)).all()]
    except:
        return [therapist.toDict() for therapist in Therapist.query.order_by(func.random()).limit(3).all()]
