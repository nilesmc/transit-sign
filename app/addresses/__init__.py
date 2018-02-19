from flask import Blueprint

bp = Blueprint('addresses', __name__)

from app.addresses import routes