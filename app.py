from flask import Flask, render_template, request
from model import rank_resumes

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    rankings = []

    if request.method == "POST":
        job_description = request.form["job_description"]
        resumes = request.files.getlist("resumes")

        rankings = rank_resumes(job_description, resumes)

    return render_template("index.html", rankings=rankings)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)