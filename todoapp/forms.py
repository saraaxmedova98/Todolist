from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from todoapp.models import User
from flask_login import current_user

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), Length(min=4 , max= 30)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_pass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit_btn = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("This username is already taken")
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("This email is already taken")

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Length(min=4 , max= 30)])
    password = PasswordField("Password", validators = [DataRequired(), Email()])
    login_btn = SubmitField("Log in")
    remember = BooleanField("Remember me" , default=False)


class TaskForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    description = TextAreaField("Description", validators = [DataRequired()])
    deadline = DateTimeField("Deadline")
    submit = SubmitField('Create Post')

class ProfileForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), Length(min=4 , max= 30)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()]) 
    update_btn = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("This username is already taken")
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("This email is already taken")

class SearchForm(FlaskForm):
    search_input = StringField("Title")
    submit = SubmitField('Search')