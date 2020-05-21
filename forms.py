from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), Length(min=4 , max= 30)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_pass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit_btn = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), Length(min=4 , max= 30)])
    password = PasswordField("Password", validators = [DataRequired()])
    login_btn = SubmitField("Sign in")
    remember = BooleanField("Remember me" , default=False)