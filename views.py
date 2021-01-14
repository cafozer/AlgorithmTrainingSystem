from flask import render_template, current_app

def home_page():
    return render_template("home.html")

def problemset_page():
    db = current_app.config["db"]
    problems = db.get_problems()
    return render_template("problemset.html", problems = problems)

def rating_page():
    return render_template("rating.html")

def profile_page():
    return render_template("profile.html")

def register_page():
    return render_template("register.html")

def login_page():
    return render_template("login.html")