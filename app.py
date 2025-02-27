import sqlite3
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    session
)
import models.database as db

app = Flask(__name__)
app.secret_key = "nuggets123"

@app.route("/", methods=["GET", "POST"])
def get_main():
    return render_template("index.html")

@app.route("/jobs", methods=["GET", "POST"])
def get_jobs():
    return render_template("jobs.html")

@app.route("/register", methods=["GET", "POST"])
def get_reg():
    return render_template("reg.html")

@app.route("/login", methods=["GET", "POST"])
def get_log():
    return render_template("log.html")

@app.route("/post", methods=["GET", "POST"])
def post_job():
    return render_template("post_job.html")

@app.route("/account", methods=["GET", "POST"])
def get_account():
    return render_template("account.html")

@app.route("/logout", methods=["GET", "POST"])
def log_out():
    return render_template("index.html")

@app.route("/details", methods=["GET", "POST"])
def get_details():
    return render_template("job_details.html")

@app.route("/search", methods=["GET", "POST"])
def search_job():
    return render_template("jobs.html")








if __name__ == "__main__":
    db.create_jobs_db()
    db.create_users_db()
    app.run(debug=True)