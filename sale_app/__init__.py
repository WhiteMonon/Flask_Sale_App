from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = "!@#$$$$$$$$$$!@$^*(loW234234)"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123123@localhost/sale_app_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
