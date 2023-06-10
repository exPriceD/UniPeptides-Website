from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    login = StringField("Login: ", id="login-input")
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember me ", default=True)


class RegisterForm(FlaskForm):
    login = StringField("Login: ", validators=[Length(min=4, max=16)], id="login-input")
    email = StringField("Email: ", validators=[Email(), Length(min=1)], id="email-input")
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=1)], id="password-input")
