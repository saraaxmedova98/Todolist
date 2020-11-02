from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_mail import Mail, Message


app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config["SECRET_KEY"] = "slahGHGTY6IY75"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345@localhost:3307/todo_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE'] = 'whoosh'

app.config['IMAGE_UPLOADS'] = '/home/sara/Documents/flask_app/todoapp/static/image'
app.config['ALLOWED_IMAGE_EXTENSIONS'] = [ 'PNG', 'JPG' , 'JPEG']

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'wactopproject@gmail.com'
app.config['MAIL_PASSWORD'] = 'wactop123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mysql = MySQL(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

from todoapp import routes