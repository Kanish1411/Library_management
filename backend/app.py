from datetime import datetime
from functools import wraps
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import hashlib, random
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role, Section
# from worker import celery_init_app
from tasks import send_email_task

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# celery = celery_init_app(app)
db.init_app(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'asdfghjklmnbvcxz'
jwt=JWTManager(app)

def auth(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args,**kwargs):
            uid=get_jwt_identity()
            u=db.session.get(User,uid)
            print(u)
            if not u:
                return make_response({"msg":"User not found"},404)
            if(not u.has_role(role)):
                return make_response({"msg":"Invalid Role"},404)
            return fn(*args,**kwargs)
        return decorator
    return wrapper

@app.route("/checkLogin",methods=["GET"])
@jwt_required()
def checkLogin():
    tk=request.headers.get("Authorization")
    tk=tk.split(" ")[1]
    u=User.query.filter_by(id=get_jwt_identity()).all()
    for i in u: 
        if i.role in [1,2,3]:
            return {"msg":"Valid"}
    return {"msg": "Invalid"}

@app.route("/checkLib",methods=["GET"])
@jwt_required()
def checkLib():
    tk=request.headers.get("Authorization")
    tk=tk.split(" ")[1]
    u=User.query.filter_by(id=get_jwt_identity()).all()
    for i in u: 
        if i.role == 2 :
            return {"msg":"Valid"}
    return {"msg": "Invalid"}


@app.route("/login", methods=["POST"])
def login():
    req = request.get_json()
    user = req.get("username")
    pwd = req.get("password")
    u = User.query.filter_by(name=user).first()
    if u and check_password_hash(u.pwd, pwd):
        if u.role==1:
           token=create_access_token(identity=u.id, additional_claims={"role": "Admin"})
           return {"message":"Admin Login",'token': token}
        if u.role==2:
           token=create_access_token(identity=u.id, additional_claims={"role": "Librarian"})
           return {"message":"Librarian Login",'token': token,"id":u.id}
        token=create_access_token(identity=u.id, additional_claims={"role": "User"})
        return {"message":"User Login",'token': token,"id":u.id}
    return {"message": "User not Found"}

@app.route("/register", methods=["POST"])
def register():
    r = request.get_json()
    u = User.query.filter_by(name=r.get("username")).first()
    if u:
        return {"message": "Username Already Exists"}
    u = User.query.filter_by(email=r.get("email")).first()
    if u:
        return {"message": "Email Already Exists"}
    u = User(name=r.get("username"), email=r.get("email"), pwd=generate_password_hash(r.get("password")), role=2)
    db.session.add(u)
    db.session.commit()
    return {"message": "registration Successful"}

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

@app.route("/change_pwd", methods=["POST"])
def change_pwd():
    u = User.query.filter_by(email=request.get_json().get("email")).first()
    u.pwd = generate_password_hash(request.get_json().get("pwd"))
    db.session.commit()
    return {"msg": "Password changed. Redirecting to login page"}

@app.route("/Lib_fetch",methods=["GET"])
@auth("Librarian")
def fetch_lib():
    s=Section.query.all()
    l=[]
    for i in s:
        l.append({"id":i.id,"name":i.name,"desc":i.desc,"date":i.date_created})
    return {"Section":l}

@app.route("/add_sec",methods=["POST"])
@auth("Librarian")
def Add_section():
    v=request.get_json()
    s=Section(name=v.get("name"),date_created= datetime.strptime(v.get("date"), "%Y-%m-%d").date(),desc=v.get("desc"))
    db.session.add(s)
    db.session.commit()
    return {"msg":"Done"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Role.query.first() is None:
            db.session.add(Role(name='Admin'))
            db.session.add(Role(name='Librarian'))
            db.session.add(Role(name='User'))
            db.session.add(User(name="Librarian", email="kanishkark1411@gmail.com", role=2, pwd=generate_password_hash("pass")))
            db.session.add(User(name="Admin", email="kanram27@gmail.com", role=1, pwd=generate_password_hash("pass")))
            db.session.commit()
    app.run(debug=True, port="5000")