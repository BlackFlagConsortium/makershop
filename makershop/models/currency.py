from .. import db


class Currency(db.Model):
    name = db.Column(db.String())
    abbreviation = db.Column(db.String(3), primary_key=True)

    def __init__(self, abbreviation, name):
        self.abbreviation = abbreviation
        self.name = name