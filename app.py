from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import os
import csv
from io import StringIO
from flask import Response
import csv
from io import StringIO
from flask import Response
import pickle
import numpy as np
from flask import Flask, render_template, request


app = Flask(__name__)
app.secret_key = '5cb5ad0e6ab42f70adf05f6c04ea0e1ca00d813b5131d58c3045d869d442349b'




# ------------------ DATABASE CONFIG ------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------ LOGIN MANAGER ------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ------------------ LOAD ML MODEL ------------------


model = pickle.load(open("model/phishing_model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

# Load accuracy
try:
    with open("model/metrics.txt", "r") as f:
        model_accuracy = f.read()
except:
    model_accuracy = "N/A"
# ------------------ DATABASE MODELS ------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_text = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

# ------------------ REGISTER ------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        # Prevent duplicate users
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists!"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

# ------------------ LOGIN ------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/dashboard")

        return "Invalid credentials!"

    return render_template("login.html")

# ------------------ DASHBOARD ------------------

@app.route("/dashboard")
@login_required
def dashboard():

    # Admin sees all logs
    if current_user.role == "admin":
        logs = PredictionLog.query.all()
    else:
        logs = PredictionLog.query.filter_by(user_id=current_user.id).all()

    total = len(logs)
    legit = len([l for l in logs if l.prediction == "Legitimate"])
    spam = len([l for l in logs if l.prediction == "Spam"])
    phishing = len([l for l in logs if l.prediction == "Phishing"])

    return render_template("dashboard.html",
                           logs=logs,
                           total=total,
                           legit=legit,
                           spam=spam,
                           phishing=phishing)
@app.route("/admin")
@login_required
def admin_panel():
    if current_user.role != "admin":
        return "Access Denied"

    users = User.query.all()
    return render_template("admin.html", users=users)
@app.route("/promote/<int:user_id>")
@login_required
def promote_user(user_id):
    if current_user.role != "admin":
        return "Access Denied"

    user = User.query.get(user_id)
    user.role = "admin"
    db.session.commit()

    return redirect("/admin")

@app.route("/export")
@login_required
def export_logs():

    if current_user.role == "admin":
        logs = PredictionLog.query.all()
    else:
        logs = PredictionLog.query.filter_by(user_id=current_user.id).all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["Email Text", "Prediction"])

    for log in logs:
        writer.writerow([log.email_text, log.prediction])

    output = si.getvalue()

    return Response(output,
                    mimetype="text/csv",
                    headers={"Content-Disposition":
                             "attachment;filename=logs.csv"})


@app.route("/analytics")
@login_required
def analytics():

    logs = PredictionLog.query.all()

    total = len(logs)
    legit = len([l for l in logs if l.prediction == "Legitimate"])
    spam = len([l for l in logs if l.prediction == "Spam"])
    phishing = len([l for l in logs if l.prediction == "Phishing"])

    phishing_rate = round((phishing / total) * 100, 2) if total > 0 else 0

    return render_template("analytics.html",
                           total=total,
                           legit=legit,
                           spam=spam,
                           phishing=phishing,
                           phishing_rate=phishing_rate)

# ------------------ NORMAL PREDICT (Form Submit) ------------------

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    email_text = request.form["email"]

    vector = vectorizer.transform([email_text])
    result = model.predict(vector)[0]

    label_map = {0: "Legitimate", 1: "Spam", 2: "Phishing"}
    prediction = label_map[result]

    log = PredictionLog(
        email_text=email_text,
        prediction=prediction,
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()

    return redirect("/dashboard")

# ------------------ AJAX PREDICT (Live Prediction) ------------------

@app.route("/predict_ajax", methods=["POST"])
@login_required
def predict_ajax():
    data = request.get_json()
    email_text = data.get("email")

    vector = vectorizer.transform([email_text])
    result = model.predict(vector)[0]

    label_map = {0: "Legitimate", 1: "Spam", 2: "Phishing"}
    prediction = label_map[result]

    log = PredictionLog(
        email_text=email_text,
        prediction=prediction,
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"prediction": prediction})

# ------------------ LOGOUT ------------------

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# ------------------ MAIN ------------------

if __name__ == "__main__":
    os.makedirs("instance", exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
