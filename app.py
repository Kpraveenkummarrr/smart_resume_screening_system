from flask import Flask, render_template, request, redirect, session, send_from_directory
import os, pickle

from utils.auth import validate_user
from utils.resume_parser import extract_text
from utils.preprocess import clean_text

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load ML model and vectorizer
model = pickle.load(open("model/resume_model.pkl", "rb"))
vectorizer = pickle.load(open("model/tfidf.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if validate_user(request.form["username"], request.form["password"]):
            session["user"] = request.form["username"]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        job_desc = request.form["job"]
        file = request.files["resume"]

        # Save uploaded resume
        filename = file.filename
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        # Extract + clean text for ML
        resume_text = clean_text(extract_text(path))
        job_text = clean_text(job_desc)

        # Combine resume + JD
        combined_text = resume_text + " " + job_text
        vector = vectorizer.transform([combined_text])

        # Predict role and score
        role = model.predict(vector)[0]
        score = max(model.predict_proba(vector)[0]) * 100

        return render_template(
            "result.html",
            role=role,
            score=round(score, 2),
            filename=filename
        )

    return render_template("upload.html")

# 🔥 Route to serve uploaded resume files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
