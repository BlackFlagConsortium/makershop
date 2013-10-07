import os

from flask import Flask


def create_app(**kwargs):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

    from .models import db

    for k, v in kwargs.items():
        app.config[k] = v

    db.init_app(app)

    app.db = db

    from . import views

    app.register_blueprint(views.users_bp, url_prefix='/user')
    app.register_blueprint(views.shop_bp, url_prefix='/shop')

    return app
