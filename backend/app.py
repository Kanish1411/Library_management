from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///DB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app=app)
CORS(app)

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    name=db.Column(db.String(10),nullable=False)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    name=db.Column(db.String(10),nullable=False)
    email=db.Column(db.String(10),nullable=False)
    pwd=db.Column(db.String(10),nullable=False)
    role=db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

@app.route("/login",methods=["POST"])
def login():
    req=request.get_json()
    user=req.get("username")
    pwd=req.get("password")
    u=User.query.filter_by(name=user).first()
    if u and check_password_hash(u.pwd,pwd):
        return {"message":"user found"}
    return {"message":"user Not found"}, 400

@app.route("/register",methods=["POST"])
def register():
    r=request.get_json()
    print(r)
    u=User.query.filter_by(name=r.get("username")).first()
    if u:
        return {"message":"Username Already Exists"}
    u=User.query.filter_by(email=r.get("email")).first()
    if u:
        return {"message":"Email Already Exists"}
    u=User(name=r.get("username"),email=r.get("email"),pwd=generate_password_hash(r.get("password")),role=2)
    db.session.add(u)
    db.session.commit()
    return {"message":"registration Succesful"}

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        if Role.query.first() is None:
            db.session.add(Role(name='Librarian'))
            db.session.add(Role(name='User'))
            db.session.add(User(name="Libraian",email="lib@123.com",role=1,pwd="pass"))
            db.session.commit()
    app.run(debug=True,port="5000")
