from todoapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique=True, nullable = False)
    email = db.Column(db.String(30), unique=True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    image = db.Column(db.String(120), nullable = True, default = "image/profile.png")
    tasks = db.relationship('Task', backref= 'person', lazy = True)

    def __repr__(self):
        return f'{self.username}'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(120), nullable = False)
    deadline = db.Column(db.DateTime, nullable = False, default= datetime.utcnow )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f'<Task({self.title}{self.deadline})>'

