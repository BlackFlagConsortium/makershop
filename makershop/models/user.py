from hashlib import sha256

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(), nullable=True)

    emails = db.relationship(
        'UserEmail',
        backref='user',
        uselist=True,
        lazy='dynamic',
    )

    def __init__(self, email, password=None, name=None):
        self.password_hash = sha256(password.encode('utf-8')).hexdigest()
        email = UserEmail(email)
        self.name = name

        db.session.add(email)
        db.session.commit()
        self.emails.append(email)

    def check_password(self, password):
        return self.password_hash == sha256(
            password.encode('utf-8')
        ).hexdigest()

    @staticmethod
    def find_by_email(email):
        """Given an email address, return to User with which it is associated
        """
        return UserEmail.query.filter_by(
            email=email
        ).one().user


class UserEmail(db.Model):
    email = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, email, user=None):
        if user:
            self.user_id = user.id
        self.email = email

    def __repr__(self):
        return '<UserEmail(uid={}, "{}")>'.format(self.user_id, self.email)