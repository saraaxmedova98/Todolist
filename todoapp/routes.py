from flask import render_template, redirect, url_for, flash, abort, request
from todoapp.forms import RegisterForm, LoginForm, TaskForm, ProfileForm, SearchForm
from todoapp import app, bcrypt , db, mysql
from todoapp.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
import copy 

@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/about')
@login_required
def about():
    task_list = Task.query.filter_by( person = current_user)
    return render_template("about.html", infos= task_list)

@app.route("/register", methods= ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password = password_hash)
        db.session.add(user)
        db.session.commit()
        flash("You successfully registered", "success")
        return redirect(url_for('login'))
    return render_template("account/register.html" , form = form)

@app.route("/login", methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('about'))    
        else:
            flash("Something went wrong. Please enter valid email or password",'danger')
    return render_template("account/login.html", form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/task/create", methods= ['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task( title = form.title.data , description = form.description.data , deadline = form.deadline.data , person = current_user )
        db.session.add(task)
        db.session.commit()
        flash("You successfully created task", "success")
        return redirect(url_for('about'))
    return render_template("account/create.html", form = form , title = 'Create')

@app.route("/task/<int:task_id>")
@login_required
def details(task_id):
    task = Task.query.get_or_404(task_id)
    if task.person != current_user:
        abort(403)
        
    return render_template("account/details.html", task = task)

@app.route('/task/<int:task_id>/update', methods= ['GET', 'POST'])
@login_required
def update(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm()
    if task.person != current_user:
        abort(403)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data
        db.session.commit()
        flash('Your task is successfully updated',"success")
        return redirect(url_for('details', task_id=task.id))
        
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.deadline.data = task.deadline
    return render_template("account/create.html" , form=form , title = 'Update', task =task)

@app.route('/task/<int:task_id>/delete', methods= ['POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.person != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your task is successfully deleted',"success")
    return redirect(url_for('about'))


@app.route("/search", methods= ['GET', 'POST'])
def search():
    form = SearchForm()
    return render_template("base.html", form = form)

@app.route("/profile/<username>", methods= ['GET', 'POST'])
@login_required
def profile(username):
    form = ProfileForm()
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename=current_user.image) 
    if form.validate_on_submit():
        # candidate = form.password.data
        candidate =copy.copy(form.password.data)
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = password_hash
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('about'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        # if bcrypt.check_password_hash(current_user.password, candidate):
        form.password.data = current_user.password
    return render_template("account/profile.html", image_file = image_file , form = form)
    



