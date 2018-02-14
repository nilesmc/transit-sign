from app import app, db, cli
from app.models import User, Stop
# from app.lib import TriMetService as TMS

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Stops': Stop, 'TMS': TMS }