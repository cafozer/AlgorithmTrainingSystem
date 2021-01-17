from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators, SelectField, SubmitField, RadioField
from flask import current_app
import server

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

class LikeDislikeForm(FlaskForm):
    likeordislike = RadioField("Like or Dislike", choices = [(1,"Like"), (0,"Dislike")])