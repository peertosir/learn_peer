from learn_peer_app import db
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, IntegerField, PasswordField, ValidationError, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from learn_peer_app.models import User


class RegisterForm(FlaskForm):
    username = StringField("Enter your username: ", validators=[DataRequired()])
    email = StringField("Enter your email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Enter your password: ", validators=[DataRequired(), EqualTo('pass_confirm')])
    pass_confirm = PasswordField("Enter your password one more time: ", validators=[DataRequired()])
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter(User.email == field.data):
            raise ValidationError("User with this email already exists")

    def check_username(self, field):
        if User.query.filter(User.username == field.data):
            raise ValidationError("User with this email already exists")


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Log in")