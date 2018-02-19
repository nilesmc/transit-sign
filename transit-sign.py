from app import create_app, db, cli
from app.models import Address, User, Stop
# from app.lib import TriMetService as TMS

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Stops': Stop, 'TMS': TMS }
