from flask_assets import Bundle, Environment
from app import app

bundles = {

    'home_js': Bundle(
        'js/transit-sign.js',
        output='gen/home.js'),

}

assets = Environment(app)

assets.register(bundles)