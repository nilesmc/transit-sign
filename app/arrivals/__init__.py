from flask import Blueprint

bp = Blueprint('arrivals', __name__)

from app.arrivals import routes