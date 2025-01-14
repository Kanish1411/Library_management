import base64
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask,  jsonify, make_response, request
from flask_caching import Cache
from flask_cors import CORS
import hashlib, random
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import Book, Lendings, Reads, db, User, Role, Section,Requests
from tasks import send_email_task, send_pdf_task
from io import BytesIO
import fitz
# from worker import celery_init_app

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# cache=Cache(config={"CACHE_TYPE":"RedisCache","CACHE_REDIS_HOST":"127.0.0.1","CACHE_REDIS_PORT":6379})
# cache.init_app(app)
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

# @cache.cached(timeout=60)
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

# @cache.cached(timeout=60)
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

@app.route("/checkAd",methods=["GET"])
@jwt_required()
def checkAd():
    tk=request.headers.get("Authorization")
    tk=tk.split(" ")[1]
    u=User.query.filter_by(id=get_jwt_identity()).all()
    for i in u: 
        if i.role == 1 :
            return {"msg":"Valid"}
    return {"msg": "Invalid"}

# @cache.cached(timeout=60)
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
    cu = get_jwt_identity()
    for section in sections:
        books = []
        us=User.query.filter_by(id=cu).first().role
        if us==3:
            b=Book.query.filter_by(sec_id=section.id,available=True).all()
        else:
            b=Book.query.filter_by(sec_id=section.id).all()
        for book in b: 
            image_base64 = base64.b64encode(book.image).decode('utf-8')
            books.append({"id": book.id,"name": book.name,"author": book.Author,"image": image_base64})
        section_list.append({"id": section.id,"name": section.name,"desc": section.desc,"date": section.date_created,"books": books})
    return {"Section": section_list}

@app.route("/sections",methods=["GET"])
@auth("Librarian")
def sections():
    l=[]
    s=Section.query.all()
    for i in s:
        l.append({"name":i.name,"id":i.id,"desc":i.desc,"date":i.date_created.strftime("%Y-%m-%d")})
    return l

@app.route("/add_sec",methods=["POST"])
@auth("Librarian")
def Add_section():
    v=request.get_json()
    s=Section(name=v.get("name"),date_created=datetime.strptime(v.get("date"), "%Y-%m-%d").date(),desc=v.get("desc"))
    db.session.add(s)
    db.session.commit()
    r=Reads(sec_id=Section.query.filter_by(name=v.get("name")).first().id)
    db.session.add(r)
    db.session.commit()
    return {"msg":"Done"}

@app.route("/update_sec",methods=["POST"])
@auth("Librarian")
def Update_sec():
    v=request.get_json()
    s=Section.query.filter_by(id=v.get("id")).first()
    s.name=v.get("name")
    s.date_created=datetime.strptime(v.get("date"), "%Y-%m-%d").date()
    s.desc=v.get("desc")
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
    section=data.get("section")
    image_bytes = base64.b64decode(image_base64)
    content_bytes = base64.b64decode(content_base64)
    new_book = Book(name=name, Author=author, image=image_bytes, content=content_bytes,sec_id=section)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book uploaded successfully!'})

@app.route("/delete_book",methods=["POST"])
@auth("Librarian")
def Delete_book():
    v=request.get_json()
    b=Book.query.filter_by(id=v.get("id")).first()
    if b:
        db.session.delete(b)
        db.session.commit()
        l=Lendings.query.filter_by(book_id=b.id).first()
        if l!=None:
            db.session.delete(l)
        r=Requests.query.filter_by(book_id=b.id).all()
        if r!=None:
            for j in r:
                db.session.delete(j)
    return {"msg":"deleted"}

@app.route("/fetch_bk_det",methods=["POST"])
def fetch_bk_det():
    book=Book.query.filter_by(id=request.get_json().get("bk_id")).first()
    r=Reads.query.filter_by(sec_id=book.sec_id).first()
    r.reads+=1
    db.session.commit()
    l=[]
    if book:
        image_base64 = base64.b64encode(book.image).decode('utf-8')
        l.append({"id": book.id,"name": book.name,"author": book.Author,"image": image_base64})
    return {"book":l}

@app.route('/book/<int:book_id>/<int:page_no>', methods=['GET'])
def get_book_page(book_id, page_no=0):
    book = Book.query.filter_by(id=book_id).first()
    r=Reads.query.filter_by(sec_id=book.sec_id).first()
    r.pg_read+=1
    db.session.commit()
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
    bk=Book.query.filter_by(id=v.get("bk_id")).first()
    r=Requests.query.filter_by(req="pdf",user_id=v.get("id"),book_id=v.get("bk_id")).first()
    if r == None:
        r=Requests(req="pdf",user_id=v.get("id"),book_id=v.get("bk_id"))
        r1=Reads.query.filter_by(sec_id=bk.sec_id).first()
        r1.pdfs+=1
        db.session.add(r)
        db.session.commit()
        return {"msg":"Book PDF request Sent"}
    return {"err":"Already Requested"}

@app.route("/req_fetch",methods=["GET"])
def req_fetch():
    r=Requests.query.filter_by(accepted=0).all()
    l=[]
    l2=[]
    for i in r:
        u=User.query.filter_by(id=i.user_id).first()
        b=Book.query.filter_by(id=i.book_id).first()
        if b!=None:
            if i.req=="pdf":
                l2.append({"id":i.id,"type":i.req,"name":u.name,"Book":b.name})
            else:
                l.append({"id":i.id,"type":i.req,"name":u.name,"Book":b.name})
    return {"Req_get":l,"Req_pdf":l2}

@app.route("/get_book",methods=["POST"])
def get_book():
    v=request.get_json()
    r=Requests.query.filter_by(req="Book",user_id=v.get("id"),book_id=v.get("bk_id")).first()
    r1=Requests.query.filter_by(user_id=v.get("id")).all()
    r2=Reads.query.filter_by(sec_id=Book.query.filter_by(id=v.get("bk_id")).first().sec_id).first()
    if  r1!=None and len(r1)>4:
        return {"err":"Requested 5 books already"}
    if r == None:
        r=Requests(req="Book",user_id=v.get("id"),book_id=v.get("bk_id"))
        r2.lends+=1
        db.session.add(r)
        db.session.commit()
        return {"msg":"Request Successful"}
    if r.accepted:
        return {"msg":"Book request accepted Already"}
    return {"err":"Already Requested"}

@app.route("/acceptreq",methods=["POST"])
@auth("Librarian")
def acceptReq():
    v=request.get_json()
    r=Requests.query.filter_by(id=v.get("id")).first()
    bk=Book.query.filter_by(id=r.book_id).first()
    if v.get("req")["type"]== "pdf":
        u=User.query.filter_by(id=r.user_id).first()
        db.session.delete(r)
        db.session.commit()
        send_pdf_task(u.email, f'Book requested {bk.name}',
                  f'The Book {bk.name} written by {bk.Author} is now for u to download and enjoy!! \n Only at Rs: 199 \n Please Complete The payment process',
                  bk.content, bk.name+".pdf")   
    else:
        l=Lendings(user_id=r.user_id,book_id=r.book_id,req_id=r.id,time_left=datetime.now()+timedelta(days=7))
        r.accepted=True
        bk.available=False
        db.session.add(l)
        db.session.commit()
    return {}

@app.route("/rejectreq",methods=["POST"])
@auth("Librarian")
def rejectReq():
    v=request.get_json()
    r=Requests.query.filter_by(id=v.get("id")).first()
    db.session.delete(r)
    db.session.commit()
    return {}

@app.route("/mybooks",methods=["POST"])
def fetch_mybooks():
    v=request.get_json()
    print(v.get("id"))
    l1=Lendings.query.filter_by(user_id=v.get("id")).all()
    l=[]
    for i in l1:
        book=Book.query.filter_by(id=i.book_id).first()
        if book:
            image_base64 = base64.b64encode(book.image).decode('utf-8')
            if(i.time_left<datetime.now()):
                db.session.delete(i)
                db.session.commit()
            if(i.time_left>datetime.now()):
                l.append({"id": book.id,"name": book.name,"author": book.Author,"image": image_base64,"timeleft":str(i.time_left-datetime.now())})
    return {"l":l}

@app.route("/return_bk",methods=["POST"])
def ret_bk():
    l=Lendings.query.filter_by(book_id=request.get_json().get("bk_id")).first()
    r=Requests.query.filter_by(id=l.req_id).first()
    bk=Book.query.filter_by(id=request.get_json().get("bk_id")).first()
    bk.available=True
    db.session.delete(l)
    db.session.delete(r)
    db.session.commit()
    return {}

@app.route("/delete_sec",methods=["POST"])
@auth("Librarian")
def delete_sec():
    v=request.get_json()
    sec=Section.query.filter_by(id=v.get("id")).first()
    bk=Book.query.filter_by(sec_id=sec.id).all()
    for i in bk:
        l=Lendings.query.filter_by(book_id=i.id).first()
        if l!=None:
            db.session.delete(l)
        r=Requests.query.filter_by(book_id=i.id).all()
        if r!=None:
            for j in r:
                db.session.delete(j)
        db.session.delete(i)
    db.session.delete(sec)
    db.session.commit()
    return {}

@app.route("/update_book", methods=["POST"])
@auth("Librarian")
def update_book():
    v = request.get_json()
    book = Book.query.get(v.get("id"))
    l=Lendings.query.filter_by(book_id=book.id).first()
    if l!=None:
            db.session.delete(l)
    r=Requests.query.filter_by(book_id=book.id).all()
    if r!=None:
            for j in r:
                db.session.delete(j)
    book.name = v.get('name')
    book.Author = v.get('author')
    book.sec_id =v.get("section")
    image_base64 = v.get('image')
    content_base64 = v.get('content')
    if image_base64!=None:
        image_bytes = base64.b64decode(image_base64)
        book.image = image_bytes
    if content_base64!=None:
        content_bytes = base64.b64decode(content_base64)
        book.content = content_bytes
    db.session.commit()
    return jsonify({})

@app.route("/fetch_book/<int:book_id>", methods=["GET"])
@auth("Librarian")
def fetch_book(book_id):
    book = Book.query.get(book_id)
    book_data = {
        'name': book.name,
        'author': book.Author,
        'section_id': book.sec_id,
    }
    return jsonify(book_data)

@app.route("/fetch_l",methods=["GET"])
@auth("Librarian")
def fetch_lend():
    le=Lendings.query.all()
    l=[]
    for i in le:
        u=User.query.filter_by(id=i.user_id).first()
        b=Book.query.filter_by(id=i.book_id).first()
        l.append({"id":i.id,"name":u.name,"bk_name":b.name,"time":str(i.time_left-datetime.now())})
    return {"l":l}

@app.route("/revoke",methods=["PUT"])
def revoke():
    v=request.get_json()
    l=Lendings.query.filter_by(id=v.get("id")).first()
    r=Requests.query.filter_by(id=l.req_id).first()
    db.session.delete(r)
    bk=Book.query.filter_by(id=l.book_id).first()
    bk.available=True
    db.session.delete(l)
    db.session.commit()
    return {}

@app.route("/search",methods=["POST"])
def search():
    v=request.get_json()
    q=v.get("query")
    l=[]
    sec=[]
    if "Section:" in q:
        u=q.split(" ")[1]
        s=Section.query.filter(Section.name.like(f"%{u}%")).all()
        for section in s:
            bk= []
            b=Book.query.filter_by(sec_id=section.id,available=True).all()
            for book in b: 
                image_base64 = base64.b64encode(book.image).decode('utf-8')
                bk.append({"id": book.id,"name": book.name,"author": book.Author,"image": image_base64})
            sec.append({"id": section.id,"name": section.name,"desc": section.desc,"date": section.date_created,"books": bk})
    b=Book.query.filter(Book.name.like(f"%{q}%"),Book.available.is_(True)).all()
    if b!=[]:
        for i in b:
            image_base64 = base64.b64encode(i.image).decode('utf-8')
            l.append({"id": i.id,"s_id":i.sec_id,"name":i.name,"author":i.Author,"image": image_base64})
    b=Book.query.filter(Book.Author.like(f"%{q}%"),Book.available.is_(True)).all()
    if b!=[]:
        for i in b:
            image_base64 = base64.b64encode(i.image).decode('utf-8')
            if ({"id": i.id,"s_id":i.sec_id,"name":i.name,"author":i.Author,"image": image_base64} not in l):
                l.append({"s_id":i.sec_id,"name":i.name,"author":i.Author,"image": image_base64})
    if l==[]:
        s=Section.query.filter(Section.name.like(f"%{q}%")).all()
        for section in s:
            bk= []
            b=Book.query.filter_by(sec_id=section.id,available=True).all()
            for book in b: 
                image_base64 = base64.b64encode(book.image).decode('utf-8')
                bk.append({"id": book.id,"name": book.name,"author": book.Author,"image": image_base64})
            sec.append({"id": section.id,"name": section.name,"desc": section.desc,"date": section.date_created,"books": bk})
    s2={}
    for i in l:
        if i["s_id"] in s2:
            s2[i["s_id"]].append(i)
        else:
            s2[i["s_id"]]=[i]
    for i in s2:
        section=Section.query.filter_by(id=i).first()
        sec.append({"id": section.id,"name": section.name,"desc": section.desc,"date": section.date_created,"books": s2[i]})
    return {"l":sec}

@app.route("/user_fetch/<int:id>",methods=["GET"])
def user_fetch(id):
    u=User.query.filter_by(id=id).first()
    le=Lendings.query.filter_by(user_id=id).all()
    l=[]
    for i in le:
        b=Book.query.filter_by(id=i.book_id).first()
        image_base64 = base64.b64encode(b.image).decode('utf-8')
        l.append({"id":i.id,"bk_name":b.name,"time":str(i.time_left-datetime.now()),"author": b.Author,"image": image_base64})
    return{"name":u.name,'l':l}

@app.route('/reads', methods=['GET'])
def get_section_reads():
    sections = Reads.query.all()
    if sections:
        section_data = []
        for section in sections:
            section_data.append({
                'sec_id': section.sec_id,
                'reads': section.reads,
                'pg_read': section.pg_read,
                'pdfs': section.pdfs,
                'lends': section.lends
            })
        return jsonify(section_data)
    else:
        return jsonify({"error": "No data found"}), 404

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