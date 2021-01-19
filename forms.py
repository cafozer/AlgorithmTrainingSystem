from flask_wtf import FlaskForm
from wtforms import Form, widgets, StringField, PasswordField, validators, SelectField, SubmitField, RadioField, BooleanField, SelectMultipleField
from flask import render_template, current_app, flash, request, url_for, redirect, g


class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])

class AddProblemForm(FlaskForm):
    problem_name = StringField("Problem Name", [validators.DataRequired()])
    problem_url = StringField("Problem Url", [validators.DataRequired()])
    problem_difficulty = SelectField("Problem Difficulty", choices=[(1,"Easy"), (2,"Medium"), (3,"Hard")])

class NewTopicForm(FlaskForm):
    topic_name = StringField("Topic Name", [validators.DataRequired()])

class SortForm(FlaskForm):
    """blank"""