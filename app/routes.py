from app import app

@app.route('/')
@app.route('/index')
def index():
  return "This is where it all starts"
