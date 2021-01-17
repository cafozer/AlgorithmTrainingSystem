from flask import render_template, current_app, flash, request, url_for, redirect, g
from flask_login import login_user, logout_user, current_user
from forms import LoginForm, AddProblemForm, LikeDislikeForm, RegisterForm
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher
from problem import Problem
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user is None:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@login_required
def logout_page():
    logout_user()
    next_page = request.args.get("next", url_for("home_page"))
    return redirect(next_page)

def home_page():
    print(current_user)
    return render_template("home.html")

@login_required
def problemset_page():
    db = current_app.config["db"]
    problems = db.sort_by_difficulty_descending()
    form = {}
    for key, problem in problems:
        newform = LikeDislikeForm()
        form[key] = newform
    for key, problem in problems:
        if form[key].validate_on_submit():
            print("validate")
        print("like or dislike cliclked")
        print(problem.name)
        print(key)
        print(form[key].data["likeordislike"])
    return render_template("problemset.html", problems = problems, form=form)

def rating_page():
    return render_template("rating.html")

def profile_page():
    return render_template("profile.html")

def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = hasher.hash(form.data["password"])
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)
    return render_template("register.html", form=form)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            print(password)
            print(user.password)
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)

def problem_add_page():
    form = AddProblemForm()
    if form.validate_on_submit():
        print("dbg")
        name = form.data["problem_name"]
        url = form.data["problem_url"]
        print(name)
        newproblem = Problem(name, url, 1, 1)
        db = current_app.config["db"]
        db.add_problem(newproblem)
        next_page = request.args.get("next", url_for("problemset_page"))
        return redirect(next_page)
    return render_template("problem_add.html", form=form)

def change_like_dislike():
    print("xd")

def like_action():
    print("like")
    return redirect(request.referrer)