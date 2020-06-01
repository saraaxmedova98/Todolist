from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config["SECRET_KEY"] = "slahGHGTY6IY75"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345@localhost:3307/todo_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mysql = MySQL(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

from todoapp import routes