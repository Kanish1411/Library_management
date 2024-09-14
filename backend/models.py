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
    def has_role(self,r):
        ri=Role.query.filter_by(name=r).first()
        if ri!=None and ri.id==self.role:
            return True
        return False
    
class Section(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    date_created=db.Column(db.Date, nullable=False)
    desc = db.Column(db.String(30), nullable=False)

class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    sec_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    Author = db.Column(db.String(20), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    content=db.Column(db.LargeBinary, nullable=True)
    available=db.Column(db.Boolean,default=True)

class Requests(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    req= db.Column(db.String(10), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id=db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    accepted=db.Column(db.Boolean,default=False)