from flask import render_template, current_app, flash, request, url_for, redirect, g
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, AddProblemForm, RegisterForm, NewTopicForm, SortForm
from user import get_user
from topic import Topic
from database import Database
from user import User
from passlib.hash import pbkdf2_sha256 as hasher
from problem import Problem
from status import Status
from wtforms import TextField, SelectField, StringField, SelectMultipleField, widgets, RadioField, validators
from wtforms.validators import ValidationError
import os

class MultiCheckboxField(SelectMultipleField):
    def pre_validate(self, form):
        """disable pre validation"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

def at_least_one(form, field):
    if len(field.data) == 0:
        raise ValidationError('Problem should have at least one topic.')

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
    for problem_key, topic_key in rels:
        relations.append((db.get_topic(topic_key).name, db.get_problem(problem_key).name))
    form = SortForm()
    if form.validate_on_submit():
        if form.data["sort_choice"] == '1':
            return redirect(url_for('problemset_page', sort="default"))
        elif form.data["sort_choice"] == '2':
            return redirect(url_for('problemset_page', sort="ascending_difficulty"))
        elif form.data["sort_choice"] == '3':
            return redirect(url_for('problemset_page', sort="descending_difficulty"))
        else:
            return redirect(url_for('problemset_page', sort="most_like"))
    return render_template("problemset.html", problems = problems, relations=relations, form=form, sort=sort)

def rating_page():
    db = current_app.config["db"]
    user_names = db.get_users_by_like()
    users = []
    for name in user_names:
        users.append(db.get_user(name[0]))
    return render_template("rating.html", users=users)

def profile_page(userid):
    print(userid)
    db = current_app.config["db"]
    curuser = db.get_user(userid)
    return render_template("profile.html", userid=userid, number_of_questions=curuser.number_of_questions_added, likes=curuser.number_of_likes, dislikes=curuser.number_of_dislikes)

def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = hasher.hash(form.data["password"])
        db = current_app.config["db"]
        db.add_user(User(username,password))
        next_page = request.args.get("next", url_for("login_page"))
        return redirect(next_page)
    return render_template("register.html", form=form)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            print("user.password:")
            #print(user.password)
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
    setattr(AddProblemForm, 'problem_topics', MultiCheckboxField('Problem Topics', choices=db.give_topics(), validators=[at_least_one]))
    form = AddProblemForm()
    if form.validate_on_submit():
        name = form.data["problem_name"]
        url = form.data["problem_url"]
        difficulty = form.data["problem_difficulty"]
        id_of_owner = db.get_user_key(current_user.username)
        newproblem = Problem(name, url, int(difficulty), id_of_owner)
        problem_id = db.add_problem(newproblem)
        for topic_id in form.data["problem_topics"]:
            db.add_problem_topic_rel(topic_id, problem_id)
        db.increase_number_of_questions(id_of_owner)
        next_page = request.args.get("next", url_for("problemset_page", sort='default'))
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
            owner_id = problem.owner_id
    db.give_like(inc)
    db.increase_likes(owner_id)
    return redirect(url_for('problemset_page', sort=nextsort))

def dislike_page(probid, nextsort):
    db = current_app.config["db"]
    problems = db.get_problems()
    for key, problem in problems:
        if problem.name == probid:
            inc = key
            owner_id = problem.owner_id
    db.give_dislike(inc)
    db.increase_dislikes(owner_id)
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
    print("cant solved")
    db = current_app.config["db"]
    problems = db.get_problems()
    for key, problem in problems:
        if problem.name == probid:
            problem_id = key
    db.add_status(Status(problem_id, db.get_user_key(current_user.username), 0))
    return redirect(url_for('problemset_page', sort=nextsort))

def problems_of_a_user(userid):
    db = current_app.config["db"]
    problems = db.get_problems_of_a_user(userid)
    rels = db.give_rels()
    relations = []
    for problem_key, topic_key in rels:
        relations.append((db.get_topic(topic_key).name, db.get_problem(problem_key).name))
    return render_template("problems_of_a_user.html", problems=problems, relations=relations)

def update_problem_page(probid):
    db = current_app.config["db"]
    setattr(AddProblemForm, 'problem_topics', MultiCheckboxField('Problem Topics', choices=db.give_topics(), default=1))
    form = AddProblemForm()
    if form.validate_on_submit():
        name = form.data["problem_name"]
        url = form.data["problem_url"]
        difficulty = form.data["problem_difficulty"]        
        id_of_owner = db.get_user_key(current_user.username)
        newproblem = Problem(name, url, int(difficulty), id_of_owner)
        problem_id = db.update_problem(newproblem, probid)
        print("problem updated")
        db.delete_relations(problem_id)
        print("relations deleted")
        for topic_id in form.data["problem_topics"]:
            db.add_problem_topic_rel(topic_id, problem_id)
        print("new relations added")
        next_page = request.args.get("next", url_for("problems_of_a_user", userid=current_user.username))
        return redirect(next_page)
    return render_template("update_problem.html", form=form)

def delete_problem_page(probid):
    db = current_app.config["db"]
    key = db.get_problem_key(probid)
    deleted_problem = db.get_problem(key)
    db.delete_relations(key)
    db.delete_status(key)
    db.delete_problem(probid)
    db.decrease_number_of_questions(current_user.username)
    db.decrease_likes(deleted_problem.likes, current_user.username)
    db.decrease_dislikes(deleted_problem.dislikes, current_user.username)
    return redirect(request.referrer)

def analyze_me_page():
    db = current_app.config["db"]
    user_id = db.get_user_key(current_user.username)
    print("db url: ")
    print(os.getenv("DATABASE_URL"))
    weak_topics = db.find_weak_topics(user_id)
    suggest_id = set()
    for topic_id, dummy in weak_topics:
        suggest = db.get_efficient_problems(topic_id)
        for problem_id in suggest:
            suggest_id.add(problem_id)
    rels = db.give_rels()
    relations = []
    for problem_key, topic_key in rels:
        relations.append((db.get_topic(topic_key).name, db.get_problem(problem_key).name))
    problems = []
    for key in suggest_id:
        problems.append((key, db.get_problem(key)))
    topics = []
    for topic_id, dummy in weak_topics:
        topics.append(db.get_topic(topic_id))
    return render_template("analyze.html", problems=problems, relations=relations, topics=topics)