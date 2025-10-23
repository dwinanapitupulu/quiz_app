from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_bcrypt import Bcrypt
from database import get_db
import requests
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret123"
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

class User(UserMixin):
    def __init__(self, id, username, password, nickname):
        self.id = id
        self.username = username
        self.password = password
        self.nickname = nickname

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user:
        return User(user["id"], user["username"], user["password"], user["nickname"])
    return None

def unix_to_local_date(ts, tz_offset_seconds):
    # convert unix timestamp + timezone offset (seconds) -> datetime
    return datetime.utcfromtimestamp(ts + tz_offset_seconds)

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    if request.method == "POST":
        city = request.form["city"]
        api_key = "xxxx"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}&lang=id"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            weather_data = None
    return render_template("weather.html", weather=weather_data)
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        nickname = request.form["nickname"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Validasi password sama
        if password != confirm_password:
            flash("Password tidak sama, coba lagi ya!")
            return redirect(url_for("register"))

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password)

        db = get_db()

        # Cek username sudah ada atau tidak
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            flash("Username sudah dipakai, coba yang lain ya!")
            return redirect(url_for("register"))

        # Cek nickname unik
        existing_nick = db.execute("SELECT * FROM users WHERE nickname = ?", (nickname,)).fetchone()
        if existing_nick:
            flash("Nickname sudah dipakai, coba yang lain 😉")
            return redirect(url_for("register"))

        # Simpan user baru
        db.execute("INSERT INTO users (username, password, nickname) VALUES (?, ?, ?)",
                   (username, hashed_password, nickname))
        db.commit()

        flash("✅ Akun berhasil dibuat! Silakan login.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()

        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and bcrypt.check_password_hash(user["password"], password):
            user_obj = User(user["id"], user["username"], user["password"], user["nickname"])
            login_user(user_obj)
            flash(f"Welcome back, {user['nickname']}! 👋")
            return redirect(url_for("home"))
        else:
            flash("Username atau password salah!")

    return render_template("login.html")

@app.route("/profile")
@login_required
def profile():
    db = get_db()

    total_score = db.execute(
        "SELECT SUM(score) as total FROM scores WHERE user_id = ?", (current_user.id,)
    ).fetchone()["total"]

    total_quiz = db.execute(
        "SELECT COUNT(*) as total FROM scores WHERE user_id = ?", (current_user.id,)
    ).fetchone()["total"]

    return render_template("profile.html",
                           username=current_user.username,
                           nickname=current_user.nickname,
                           total_score=total_score or 0,
                           total_quiz=total_quiz or 0)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Kamu sudah logout.")
    return redirect(url_for("home"))
    
from flask_login import login_required, current_user

questions = [
    {"question": "Apa itu Artificial Intelligence?",
     "options": ["Mesin mencetak dokumen", "Kemampuan mesin meniru kecerdasan manusia", "Komputer rusak"],
     "answer": "Kemampuan mesin meniru kecerdasan manusia"},

    {"question": "Library Python yang sering digunakan untuk AI adalah?",
     "options": ["NumPy", "TensorFlow", "Pandas", "Semua benar"],
     "answer": "Semua benar"},

    {"question": "Model AI belajar dari ...",
     "options": ["data", "warna", "kabel", "suara pintu"],
     "answer": "data"},

    {"question": "Framework AI buatan Google adalah?",
     "options": ["TensorFlow", "Laravel", "React", "Flask"],
     "answer": "TensorFlow"},
]




@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    db = get_db()

    # Saat submit
    if request.method == "POST":
        score = 0
        question_ids = session.get("quiz_questions", [])  # pakai soal yang sama
        questions = db.execute(f"SELECT * FROM questions WHERE id IN ({','.join(['?']*len(question_ids))})", question_ids).fetchall()

        for i, q in enumerate(questions):
            user_answer = request.form.get(f"q{i}")
            if user_answer.strip() == q["answer"].strip():
                score += 10  # 10 poin per soal

        # Simpan skor
        db.execute("INSERT INTO scores (user_id, score) VALUES (?, ?)", (current_user.id, score))
        db.commit()

        flash(f"Skor kamu: {score} ✅")
        return redirect(url_for("result", score=score))

    # Saat mulai kuis → ambil soal random dan simpan id soalnya
    questions = db.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 8").fetchall()
    session["quiz_questions"] = [str(q["id"]) for q in questions]  # simpan id soal

    return render_template("quiz.html", questions=questions)
    





@app.route("/result")
@login_required
def result():
    score = request.args.get("score")
    return render_template("result.html", score=score)


@app.route("/leaderboard")
@login_required
def leaderboard():
    db = get_db()
    leaders = db.execute("""
        SELECT users.nickname, 
               SUM(scores.score) AS total_score,
               COUNT(scores.id) AS total_quiz
        FROM scores
        JOIN users ON scores.user_id = users.id
        GROUP BY users.id
        ORDER BY total_score DESC
        LIMIT 10
    """).fetchall()

    return render_template("leaderboard.html", leaders=leaders)


@app.route("/weather", methods=["GET", "POST"])
def weather():
    weather_data = None
    if request.method == "POST":
        city = request.form["city"]
        api_key = "xxxxx"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}&lang=id"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            weather_data = None
    return render_template("weather.html", weather=weather_data)
    
if __name__ == "__main__":
    app.run(debug=True)

