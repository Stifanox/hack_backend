from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import users
from app.api import anonim_messages
