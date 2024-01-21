from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import users
from app.api import daily_updates
from app.api import habits
from app.api import cheerups
from app.api import therapists
