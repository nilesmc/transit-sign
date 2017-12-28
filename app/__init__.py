from flask import Flask
from config import Config
# from ipython import embed
from tri_met_service import TriMetService
from flask import Blueprint

bp = Blueprint('api', __name__)

app = Flask(__name__)
app.config.from_object(Config)

from app import routes