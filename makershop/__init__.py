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

    from .views import users, shop

    app.register_blueprint(users.bp, url_prefix='/user')
    app.register_blueprint(shop.bp, url_prefix='/shop')

    return app
