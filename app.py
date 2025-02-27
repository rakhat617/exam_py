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
import os

app = Flask(__name__)
app.secret_key = "nuggets123"
app.config['UPLOAD_FOLDER'] = 'static/images' 
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 

@app.route("/", methods=["GET", "POST"])
def get_main():
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    cursor.execute(" SELECT * FROM jobs ")
    jobs = cursor.fetchall()
    connection.close()
    jobs = jobs[:-4:-1]
    print(jobs)
    return render_template("index.html", jobs = jobs)

@app.route("/jobs", methods=["GET", "POST"])
def get_jobs():
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    cursor.execute(" SELECT * FROM jobs ")
    jobs = cursor.fetchall()
    connection.close()
    print(jobs)
    return render_template("jobs.html", jobs = jobs)

@app.route("/register", methods=["GET", "POST"])
def get_reg():
    if request.method == "POST":
        email = request.form.get("email", type=str)
        password = request.form.get("password", type=str)
        password_confirm = request.form.get("password_confirm", type=str)
        name = request.form.get("name", type=str)
        surname = request.form.get("surname", type=str)
        if password == password_confirm:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password, name, surname) VALUES (?, ?, ?, ?)', (email, password, name, surname))
            session["email"] = email
            session["name"] = name
            session["name"] = surname
            conn.commit()
            conn.close()
            return redirect(url_for("get_account"))
        else:
            error_message = "Passwords does not match. Try again"
            return render_template('reg.html', error=error_message)
    return render_template('reg.html')

@app.route("/login", methods=["GET", "POST"])
def get_log():
    if request.method == "POST":
        email = request.form.get("email", type=str)
        password = request.form.get("password", type=str)
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["email"] = user[1]
            print(session["email"])
            session["name"] = user[3]
            session["surname"] = user[4]
            return redirect(url_for("get_account"))
        else:
            error_message = "Incorrect email or password"
            return render_template('log.html', error=error_message)
    return render_template('log.html')

@app.route("/post", methods=["GET", "POST"])
def post_job():
    try:
        if session["email"]:
            if request.method == "POST":
                title = request.form.get("title", type=str)
                experience = request.form.get("experience", type=str)
                employment = request.form.get("employment", type=str)
                format_ = request.form.get("format", type=str)
                city = request.form.get("city", type=str)
                description = request.form.get("description", type=str)
                salary = request.form.get("salary", type=str)
                conn = sqlite3.connect("jobs.db")
                cursor = conn.cursor()
                cursor.execute('INSERT INTO jobs (email, title, experience, employment, format, city, description, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                            (session["email"], title, experience, employment, format_, city, description, salary ))
                conn.commit()
                conn.close()
                return redirect(url_for("get_account"))
    except:
        return redirect(url_for("get_log"))
    return render_template("post_job.html")

@app.route("/account", methods=["GET", "POST"])
def get_account():
    try:
        if session["email"]:
            name = session["name"]
            surname = session["surname"]
            email = session["email"]
            connection = sqlite3.connect("jobs.db")
            cursor = connection.cursor()
            cursor.execute(" SELECT * FROM jobs ")
            jobs = cursor.fetchall()
            connection.close()
            user_jobs = []
            for job in jobs:
                if job[1] == session["email"]:
                    user_jobs.append(job)
            return render_template("account.html", name = name, surname = surname, email = email, jobs = user_jobs)
    except:
        return redirect(url_for("get_log"))

@app.route("/logout", methods=["GET", "POST"])
def log_out():
    session.pop("email", None)
    session.pop("name", None)
    session.pop("surname", None)
    return render_template("index.html")

@app.route("/details/<id>", methods=["GET", "POST"])
def get_details(id):
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    cursor.execute(" SELECT * FROM jobs WHERE id = ?", (id,))
    job = cursor.fetchone()
    connection.close()
    return render_template("job_details.html", job = job)

@app.route("/search", methods=["GET", "POST"])
def search_results():
    search_query = request.form.get("search", type=str)
    search_location = request.form.get("location")
    print(search_query)
    connection = sqlite3.connect("jobs.db") 
    cursor = connection.cursor()
    cursor.execute(" SELECT * FROM jobs ")
    jobs = cursor.fetchall()
    jobs_catched = []
    for i in jobs: 
        if (search_query.lower() in i[2].lower() or search_query.lower() in i[7].lower()) and search_location in i[6]:
            jobs_catched.append(i)
    connection.close()
    return render_template("jobs.html", jobs = jobs_catched)

@app.route("/message", methods=["GET", "POST"])
def message():
    try:
        if session["email"]:
            if request.method == "POST":
                message = request.form.get("message", type = str)
                email = session["email"]
                confirmation = "Your candidature has been sent!"
                return render_template("job_details.html", user_message = message, user_email = email, confirmation = confirmation)
    except:
        return redirect(url_for("get_log"))

# @app.route("/add", methods=["GET", "POST"])
# def add():
#     return render_template("add_pic.html")

# @app.route("/addpic", methods=["GET", "POST"])
# def add_pic():
#     image_file = request.files['image']
#     filename = None
#     if image_file:
#         filename = image_file.filename
#         image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     connection = sqlite3.connect("jobs.db") 
#     cursor = connection.cursor()
#     cursor.execute('INSERT INTO users (image) VALUES (?)', (filename))
#     re

if __name__ == "__main__":
    db.create_jobs_db()
    db.create_users_db()
    app.run(debug=True)