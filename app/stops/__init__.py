from flask import Blueprint

bp = Blueprint('stops', __name__)

from app.stops import routes