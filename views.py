from flask import render_template, current_app, flash, request, url_for, redirect
from flask_login import login_user, logout_user
from forms import LoginForm
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher


def home_page():
    return render_template("home.html")

def problemset_page():
    db = current_app.config["db"]
    problems = db.sort_by_difficulty_descending()
    return render_template("problemset.html", problems = problems)

def rating_page():
    return render_template("rating.html")

def profile_page():
    return render_template("profile.html")

def register_page():
    return render_template("register.html")

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)