from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

##DB setup
db = SQLAlchemy(app)
Migrate(app, db)
##

##login manager init
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
###
from learn_peer_app.models import User, Lecture, Task, Course
from learn_peer_app.users.views import users
from learn_peer_app.core.views import core
app.register_blueprint(users)
app.register_blueprint(core)