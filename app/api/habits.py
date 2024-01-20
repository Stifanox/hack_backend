from app.api import bp
from app.models import Habits
from flask import request
from app.common.response import SuccessHabit, ErrorHabit
from app import db


@bp.route("/habits", methods=["POST"])
def createNewHabit():
    if request.content_type != "application/json":
        return ErrorHabit("Content type is not application/json").__dict__, 404

    if "habitId" not in request.json or "userId" not in request.json:
        return ErrorHabit("Not all required params was passed (userId, habitId)").__dict__, 404

    newHabit = Habits(user_id=request.json["userId"], habit_id=request.json["habitId"])

    db.session.add(newHabit)
    db.session.commit()

    return SuccessHabit("Habit was added successfully").__dict__, 200


@bp.route("/habits", methods=["PUT"])
def updateHabit():
    if request.content_type != "application/json":
        return ErrorHabit("Content type is not application/json").__dict__, 404

    if "id" not in request.json or "broken" not in request.json:
        return ErrorHabit("Not all required params was passed (id, broken)").__dict__, 404

    habit = Habits.query.filter_by(id=request.json["id"]).first()

    if not habit:
        return ErrorHabit("Habit was not found").__dict__, 404

    habit.broken = request.json["broken"]
    db.session.commit()
    return SuccessHabit("Habit was successfully updated").__dict__, 200


@bp.route("/habits/<int:user_id>", methods=["GET"])
def getUserHabits(user_id):
    userHabits = Habits.query.filter_by(user_id=user_id).all()

    return SuccessHabit([user.toDict() for user in userHabits]).__dict__


@bp.route("/habits", methods=["GET"])
@bp.route("/habits/", methods=["GET"])
def getUserHabitsError():
    return ErrorHabit("User id was not passed to url (/habits/<user_id>").__dict__, 404

