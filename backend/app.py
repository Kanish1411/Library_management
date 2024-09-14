import base64
from datetime import datetime
from functools import wraps
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import hashlib, random
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import Book, db, User, Role, Section
# from worker import celery_init_app
from tasks import send_email_task, send_pdf_task
from io import BytesIO

import fitz

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
    u = User(name=r.get("username"), email=r.get("email"), pwd=generate_password_hash(r.get("password")), role=3)
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

@app.route("/Lib_fetch", methods=["GET"])
@jwt_required()
def fetch_lib():
    sections = Section.query.all()
    section_list = []
    for section in sections:
        books = []
        b=Book.query.filter_by(sec_id=section.id,available=True).all()
        for book in b: 
            image_base64 = base64.b64encode(book.image).decode('utf-8')
            books.append({"id": book.id,"name": book.name,"author": book.Author,"image": image_base64})
        section_list.append({"id": section.id,"name": section.name,"desc": section.desc,"date": section.date_created,"books": books})
    return {"Section": section_list}

@app.route("/add_sec",methods=["POST"])
@auth("Librarian")
def Add_section():
    v=request.get_json()
    s=Section(name=v.get("name"),date_created=datetime.strptime(v.get("date"), "%Y-%m-%d").date(),desc=v.get("desc"))
    db.session.add(s)
    db.session.commit()
    return {"msg":"Done"}

@app.route("/upload_book",methods=["POST"])
@auth("Librarian")
def upload_book():
    data = request.get_json()
    name = data.get('name')
    author = data.get('author')
    image_base64 = data.get('image')
    content_base64 = data.get('content')
    image_bytes = base64.b64decode(image_base64)
    content_bytes = base64.b64decode(content_base64)
    new_book = Book(name=name, Author=author, image=image_bytes, content=content_bytes)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book uploaded successfully!', 'book_id': new_book.id})

@app.route("/delete_book",methods=["POST"])
@auth("Librarian")
def Delete_book():
    v=request.get_json()
    b=Book.query.filter_by(id=v.get("id")).first()
    if b:
        db.session.delete(b)
        db.session.commit()
    return {"msg":"deleted"}
@app.route("/fetch_bk_det",methods=["POST"])
def fetch_bk_det():
    print(request.get_json().get("bk_id"))
    book=Book.query.filter_by(id=request.get_json().get("bk_id")).first()
    l=[]
    if book:
        image_base64 = base64.b64encode(book.image).decode('utf-8')
        # sec=Section.quer
        l.append({"id": book.id,"name": book.name,"author": book.Author,"image": image_base64})
    return {"book":l}

@app.route('/book/<int:book_id>/<int:page_no>', methods=['GET'])
def get_book_page(book_id, page_no=0):
    book = Book.query.filter_by(id=book_id).first()
    if book and book.content:
        try:
            pdf_stream = BytesIO(book.content)
            doc = fitz.open(stream=pdf_stream, filetype="pdf")
            if page_no < 0 or page_no >= len(doc):
                return jsonify({'error': 'Invalid page number'})
            page = doc.load_page(page_no)  
            pix = page.get_pixmap() 
            img_byte_arr = BytesIO(pix.tobytes(output="png"))
            img_byte_arr.seek(0)
            img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            return jsonify({'book_id': book_id,'page_no': len(doc),'page_image': img_base64})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Book not found or no content available'})

@app.route("/request_book",methods=["POST"])
def request_book():
    v=request.get_json()
    u=User.query.filter_by(id=v.get("id")).first()
    bk=Book.query.filter_by(id=v.get("bk_id")).first()
    send_pdf_task(u.email, f'Book requested {bk.name}',
                  f'The Book {bk.name} written by {bk.Author} is now for u to download and enjoy!! \n Only at Rs: 199 \n Please Complete The payment process',
                  bk.content, bk.name+".pdf")
    return {"msg":"Book sent to Your mail"}

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