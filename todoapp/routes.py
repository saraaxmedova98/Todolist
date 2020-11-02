from flask import render_template, redirect, url_for, flash, abort, request
from todoapp.forms import RegisterForm, LoginForm, TaskForm, ProfileForm
from todoapp import app, bcrypt , db, mysql
from todoapp.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
import copy 
import os
import datetime

mail = Mail(app)

 
@app.template_filter('date')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime('%b,%e %Y')

@app.route('/')
@app.route("/home/")
def home():
    return render_template("home.html")

@app.route('/tasks/')
@login_required
def tasks():
    page = request.args.get('page', 1, type=int)
    task_list = Task.query.order_by(Task.deadline.desc()).paginate(page=page,per_page=4)
    return render_template("tasks.html", infos= task_list)


@app.route('/tasks/<username>/')
@login_required
def user_tasks(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    task_list = Task.query.filter_by(user_id = user.id).order_by(Task.deadline.desc()).paginate(page=page,per_page=4)
    return render_template("tasks.html", infos= task_list)


@app.route("/register", methods= ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password = password_hash)

        db.session.add(user)
        db.session.commit()
        msg = Message('Hello', sender = 'wactopproject@gmail.com', recipients = [form.email.data])
        msg.body = "http://localhost:5000/login"
        mail.send(msg)
        flash("You successfully registered", "success")
        return redirect(url_for('login'))
    return render_template("account/register.html" , form = form)


@app.route("/login", methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('tasks'))    
        else:
            flash("Something went wrong. Please enter valid email or password",'danger')
    return render_template("account/login.html", form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/task/create/", methods= ['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        print(form)
        task = Task( title = form.title.data , description = form.description.data ,deadline=form.deadline.data, user_id = current_user.id )
        db.session.add(task)
        db.session.commit()
        flash("You successfully created task", "success")
        return redirect(url_for('tasks'))
    return render_template("account/create.html", form = form , title = 'Create')

@app.route("/task/<int:task_id>")
@login_required
def details(task_id):
    task = Task.query.get_or_404(task_id)
    # if task.person != current_user:
    #     abort(403)
        
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
    return redirect(url_for('tasks'))

@app.route("/search", methods= ['GET', 'POST'])
def search():
    search_word = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    # task = Task.query.filter_by(person = current_user)
    searched_task = Task.query.filter(Task.title.contains(search_word)).paginate(page=page,per_page=4)
    return render_template("tasks.html", infos = searched_task)

@app.route("/profile/<username>/")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("profile.html" )

def allowed_image(filename):
    if not '.' in  filename:
        return False
    
    extension = filename.rsplit('.', 1)[1]
    if extension.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    return False

@app.route("/profile/<username>/update", methods= ['GET', 'POST'])
@login_required
def update_profile(username):
    form = ProfileForm()
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(request.args.get('image') , '=================')
        # password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.username = form.username.data
            current_user.email = form.email.data
            if request.files['image']:
                image = request.files['image']
                current_user.image = image.filename
                image.save(os.path.join(app.config['IMAGE_UPLOADS'] , image.filename))
                # print(image)
                if not allowed_image(image.filename):
                    flash('Choosen file is not image', 'danger')
                    return redirect(request.url)

            # current_user.password = password_hash
            db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(request.url)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        # form.password.data = current_user.password
    return render_template("account/update_profile.html" , form = form)

@app.route('/profile/<int:user_id>/delete', methods= ['POST'])
@login_required
def delete_profile(user_id):
    user = User.query.get_or_404(user_id)
    task = Task.query.filter_by(user_id = current_user.id)
    if user.username != current_user.username:
        abort(403)
    # for t in task:
    #     db.session.delete(t)
    db.session.delete(task) 
    db.session.delete(user)
    db.session.commit()
    flash('Your account is successfully deleted',"success")
    return redirect(url_for('login'))



