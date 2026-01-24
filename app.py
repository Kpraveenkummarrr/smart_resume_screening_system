from flask import Flask, render_template, request, redirect, session
import os, pickle

from utils.auth import validate_user
from utils.resume_parser import extract_text
from utils.preprocess import clean_text

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = pickle.load(open("model/resume_model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if validate_user(request.form["username"], request.form["password"]):
            session["user"] = request.form["username"]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        job_desc = request.form["job"]
        file = request.files["resume"]

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        text = clean_text(extract_text(path))
        prediction = model.predict([text])[0]
        score = max(model.predict_proba([text])[0]) * 100

        return render_template(
            "result.html",
            role=prediction,
            score=round(score, 2)
        )

    return render_template("upload.html")

app.run(debug=True)
