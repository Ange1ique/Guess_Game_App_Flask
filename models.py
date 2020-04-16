from Guess_Game import db
from sqlalchemy.dialects.postgresql import JSON

class Animals(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    json_animals = db.Column(db.JSON)

    def __init__(self, json_animals):
        self.json_animals = json_animals

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'json_animals': self.json_animals
        }
