from flask import render_template, current_app, flash, request, url_for, redirect, g
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, AddProblemForm, RegisterForm, NewTopicForm, SortForm
from user import get_user
from topic import Topic
from passlib.hash import pbkdf2_sha256 as hasher
from problem import Problem
from status import Status
from wtforms import TextField, SelectField, StringField, SelectMultipleField, widgets, RadioField


class MultiCheckboxField(SelectMultipleField):
    def pre_validate(self, form):
        """disable pre validation"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

@login_required
def logout_page():
    logout_user()
    flash("You have logged out.")
    next_page = request.args.get("next", url_for("home_page"))
    return redirect(next_page)

def home_page():
    print(current_user)
    return render_template("home.html")

@login_required
def problemset_page(sort):
    print(sort)
    db = current_app.config["db"]
    if sort == 'default':
        problems = db.get_problems()
        setattr(SortForm, 'sort_choice', RadioField("Sort Choice", choices=[(1, "Default"), (2, "Sort by Difficulty (Ascending)"), (3, "Sort by Difficulty (Descending)"), (4, "Sort by likes")], default=1))
    if sort == 'ascending_difficulty':
        problems = db.sort_by_difficulty_ascending()
        setattr(SortForm, 'sort_choice', RadioField("Sort Choice", choices=[(1, "Default"), (2, "Sort by Difficulty (Ascending)"), (3, "Sort by Difficulty (Descending)"), (4, "Sort by likes")], default=2))
    if sort == 'descending_difficulty':
        problems = db.sort_by_difficulty_descending()
        setattr(SortForm, 'sort_choice', RadioField("Sort Choice", choices=[(1, "Default"), (2, "Sort by Difficulty (Ascending)"), (3, "Sort by Difficulty (Descending)"), (4, "Sort by likes")], default=3))
    if sort == 'most_like':
        problems = db.sort_by_likes()
        setattr(SortForm, 'sort_choice', RadioField("Sort Choice", choices=[(1, "Default"), (2, "Sort by Difficulty (Ascending)"), (3, "Sort by Difficulty (Descending)"), (4, "Sort by likes")], default=4))
    rels = db.give_rels()
    relations = []
    for topic_key, problem_key in rels:
        relations.append((db.get_topic(topic_key).name, db.get_problem(problem_key).name))
    form = SortForm()
    if form.validate_on_submit():
        print(form.data["sort_choice"])
        if form.data["sort_choice"] == '1':
            return redirect(url_for('problemset_page', sort="default"))
        elif form.data["sort_choice"] == '2':
            return redirect(url_for('problemset_page', sort="ascending_difficulty"))
        elif form.data["sort_choice"] == '3':
            print("dbggggggggggggggg")
            return redirect(url_for('problemset_page', sort="descending_difficulty"))
        else:
            return redirect(url_for('problemset_page', sort="most_like"))
    return render_template("problemset.html", problems = problems, relations=relations, form=form, sort=sort)

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
        return redirect(url_for('register_page'))
    return render_template("register.html", form=form)

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

@login_required
def problem_add_page():
    db = current_app.config["db"]
    setattr(AddProblemForm, 'problem_topics', MultiCheckboxField('Problem Topics', choices=db.give_topics()))
    form = AddProblemForm()
    if form.validate_on_submit():
        name = form.data["problem_name"]
        url = form.data["problem_url"]
        difficulty = form.data["problem_difficulty"]
        print(form.data["problem_topics"])
        
        id_of_owner = db.get_user_id_num(current_user.username)
        newproblem = Problem(name, url, int(difficulty), id_of_owner)
        problem_id = db.add_problem(newproblem)
        for topic_id in form.data["problem_topics"]:
            db.add_problem_topic_rel(topic_id, problem_id)
        next_page = request.args.get("next", url_for("problemset_page"))
        return redirect(next_page)
    return render_template("problem_add.html", form=form)

def new_topic_page():
    form = NewTopicForm()
    if form.validate_on_submit():
        name = form.data["topic_name"]
        db = current_app.config["db"]
        newtopic = Topic(name)
        db.add_topic(newtopic)
        return redirect(url_for('problem_add_page'))
    return render_template("addnewtopic.html", form=form)

def like_page(probid, nextsort):
    db = current_app.config["db"]
    problems = db.get_problems()
    for key, problem in problems:
        if problem.name == probid:
            inc = key
    db.give_like(inc)
    return redirect(url_for('problemset_page', sort=nextsort))

def dislike_page(probid, nextsort):
    db = current_app.config["db"]
    problems = db.get_problems()
    for key, problem in problems:
        if problem.name == probid:
            inc = key
    db.give_dislike(inc)
    return redirect(url_for('problemset_page', sort=nextsort))

def solved_page(probid, nextsort):
    db = current_app.config["db"]
    problems = db.get_problems()
    for key, problem in problems:
        if problem.name == probid:
            problem_id = key
    db.add_status(Status(problem_id, db.get_user_key(current_user.username), 1))
    return redirect(url_for('problemset_page', sort=nextsort))

def cant_solved_page(probid, nextsort):
    db = current_app.config["db"]
    problems = db.get_problems()
    for key, problem in problems:
        if problem.name == probid:
            problem_id = key
    db.add_status(Status(problem_id, db.get_user_key(current_user.username), 0))
    return redirect(url_for('problemset_page', sort=nextsort))