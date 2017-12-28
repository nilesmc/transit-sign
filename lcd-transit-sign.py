from app import app, db
from app.models import User, Stop

# tri_met_service

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Stops': Stop }