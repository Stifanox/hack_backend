from app import db
from app.api import bp
from app.models import User, AnonimMessage
from flask import jsonify, request


@bp.route("/anonim-messages", methods=["POST"])
def create_message():
    data = request.get_json() or {}
    if 'senderId' not in data or 'receiverId' not in data or 'message' not in data:
        return jsonify({'error': 'missing fields'}), 400
    message = AnonimMessage()
    message.fromDict(data)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.toDict()), 201


@bp.route("/anonim-messages/user/<int:user_id>", methods=["GET"])
def get_messages_for_user(user_id):
    messages = AnonimMessage.query.filter(
        (AnonimMessage.sender_id == user_id) | (AnonimMessage.receiver_id == user_id)
    ).all()
    return jsonify([message.toDict() for message in messages])


@bp.route("/anonim-messages/sender/<int:sender_id>", methods=["GET"])
def get_messages_by_sender(sender_id):
    messages = AnonimMessage.query.filter_by(sender_id=sender_id).all()
    return jsonify([message.toDict() for message in messages])


@bp.route("/anonim-messages/receiver/<int:receiver_id>", methods=["GET"])
def get_messages_by_receiver(receiver_id):
    messages = AnonimMessage.query.filter_by(receiver_id=receiver_id).all()
    return jsonify([message.toDict() for message in messages])
