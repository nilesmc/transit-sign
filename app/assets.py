from flask_assets import Bundle, Environment
from .. import app

bundles = {

    'home_js': Bundle(
        'js/lib/jquery-1.10.2.js',
        'js/transit-sign.js',
        output='gen/home.js'),

}

assets = Environment(app)

assets.register(bundles)