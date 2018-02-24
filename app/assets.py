from flask_assets import Bundle
from app import assets

bundles = {

    'home_js': Bundle(
        'js/transit-sign.js',
        output='gen/home.js'),

    'common_css': Bundle(
      'styles/layout.scss',
        filters='sccs',
        output='public/css/common.css'
    )

}

# assets = Environment(app)

assets.register(bundles)