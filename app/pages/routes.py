import app
from app.pages import bp
from flask import render_template

# No Login Required
@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('pages/index.html', title='Home')

@bp.route('/about', methods=['GET'])
def about():
    return render_template('pages/about.html', title='About')