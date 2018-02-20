from flask_assets import Bundle
from app import assets

bundles = {

    'home_js': Bundle(
        'js/transit-sign.js',
        output='gen/home.js'),

}

# assets = Environment(app)

assets.register(bundles)