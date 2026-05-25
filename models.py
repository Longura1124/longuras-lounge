from ext import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    store = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20), nullable=False)