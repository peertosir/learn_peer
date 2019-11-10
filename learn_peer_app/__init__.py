from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

##DB setup
db = SQLAlchemy(app)
Migrate(app=app,db=db)
##

##login manager init
login_manager = LoginManager()
login_manager.init_app(app)
###

