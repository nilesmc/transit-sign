import app
from flask import render_template

# No Login Required
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('pages/index.html', title='Home')

@app.route('/about', methods=['GET'])
def about():
    return render_template('pages/about.html', title='About')