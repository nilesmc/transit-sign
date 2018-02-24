from flask_assets import Bundle
from app import assets

bundles = {

    'home_js': Bundle(
        'js/transit-sign.js',
        output='public/js/home.js'),

    'common_css': Bundle(
      'styles/layout.scss',
        filters='sccs',
        output='public/css/common.css'
    )

}

assets.register(bundles)