from hashlib import sha256

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), unique=True)

    def __init__(self, email, password=None, name=None):
        self.password_hash = sha256(password.encode('utf-8')).hexdigest()
        self.name = name
        self.email = email

    def check_password(self, password):
        return self.password_hash == sha256(
            password.encode('utf-8')
        ).hexdigest()