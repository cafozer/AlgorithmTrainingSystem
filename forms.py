from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])