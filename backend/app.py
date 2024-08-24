from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


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
    u=User.query.filter_by(name=user).all()
    if u:
        return {"message":"user found"}
    return {"message":"user Not found"}, 400
if __name__=="__main__":
    with app.app_context():
        db.create_all()
        if Role.query.first() is None:
            db.session.add(Role(name='Librarian'))
            db.session.add(Role(name='User'))
            db.session.add(User(name="Libraian",email="lib@123.com",role=1,pwd="pass"))
            db.session.commit()
    app.run(debug=True,port="5000")
