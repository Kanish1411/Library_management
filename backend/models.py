from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(10), nullable=False)
    pwd = db.Column(db.String(10), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Section(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    date_created=db.Column(db.Date, nullable=False)
    desc = db.Column(db.String(30), nullable=False)



