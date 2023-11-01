# import os untuk mengakses system database
import os

# import SQL untuk menggunakan bahasa SQL dalam python
from cs50 import SQL
# import tools untuk website
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# mengatur nama aplikasi
app = Flask(__name__)

# dipakai untuk koneksi ke database
db = SQL("sqlite:///birthdays.db")
app.config.update(SECRET_KEY=os.urandom(24))

@app.route("/", methods=["GET", "POST"])
# ketika route "/" dipanggil/diakses, maka fungsi index() dieksekusi
def index():
    # jika request yg dilakukan oleh pengguna adalah post, maka eksekusi kode dalam if
    if request.method == "POST":

        # Access form data / membaca data yang diisilkan pada form
        name = request.form.get("name")# ambil data dari input name
        month = request.form.get("month")# ambil data dari imput month
        day = request.form.get("day")# ambil data dari input day

        # insert data into database, masukkan data name, month, day ke database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        # Go back to homepage
        return redirect("/")

    else:

        # ambil seluruh data dari tabel birthdays, simpan di variabel birthdays
        birthdays = db.execute("SELECT * FROM birthdays")    

        # salin isi variabel birthdays ke birthdays, lalu kirim ke index.html
        return render_template("index.html", birthdays=birthdays)

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_data(id):
    if request.method == "GET":
        bday = db.execute("SELECT * from birthdays WHERE id = ?", id)[0]
        print(bday)
        return render_template("edit.html",bday=bday)
    elif request.method == "POST":
        bday_name = request.form.get("name")
        bday_month = request.form.get("month")
        bday_day = request.form.get("day")
        db.execute('UPDATE birthdays set name = ?, month = ?, day = ? where id = ?', bday_name, bday_month, bday_day, id)
        return redirect("/")
    
@app.route("/Delete/<id>", methods=["GET"])
def Delete(id):
    db.execute("Delete from birthdays where id = ?", id)
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    """register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"
        
        rows = db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")
        
        hash = generate_password_hash(password)
        if len(rows) == 1:
            return "username already taken"
        if password == password_repeat:
            db.execute("INSERT INTO user(username, password, email) VALUES(?, ?, ?)", username, hash, email)
            
            registered_user = db.execute("SELECT * FROM user where username = ?", username)
            session["user_id"] = registered_user[0]["id"]
            flash('you were successfully registered')
            return redirect("/")
        else:
            return "must provide matching password"
    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    """register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"
        
        rows = db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))
        
        if len(rows) !=1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return "invailid username and/or password"
        session["user_id"] = rows[0]["id"]
        
        return redirect("/")
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""
    
    session.clear()
    return redirect("/")