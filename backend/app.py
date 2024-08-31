from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
from werkzeug.security import generate_password_hash,check_password_hash
from worker import celery_init_app
from tasks import send_email_task
import random
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///DB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app=app)

celery=celery_init_app(app)
celery.set_default()

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

@app.route("/forgot_pwd",methods=["POST"])
def forgot_pwd():
    u=User.query.filter_by(email=request.get_json().get("email")).first()
    if u==None:
        return {"msg":"Email Not found"}
    otp =str( random.randint(100000, 999999))
    print(otp)
    h=hashlib.sha256(otp.encode()).hexdigest()
    # send_email_task.delay("kanishkark1411@gmail.com", 'Your OTP Code', f'Your OTP code is {otp}')
    send_email_task(u.email, 'Your OTP Code', f'Your OTP code to change password is {otp}')
    return {"msg":"An OTP is sent to your email","hash":h}

@app.route("/change_pwd",methods=["POST"])
def change_pwd():
    u=User.query.filter_by(email=request.get_json().get("email")).first()
    u.pwd=generate_password_hash(request.get_json().get("pwd"))
    db.session.commit()
    return {"msg":"Password changes Redirecting to login page"}

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        if Role.query.first() is None:
            db.session.add(Role(name='Librarian'))
            db.session.add(Role(name='User'))
            db.session.add(User(name="Libraian",email="kanishkark1411@gmail.com",role=1,pwd="pass"))
            db.session.commit()
    app.run(debug=True,port="5000")