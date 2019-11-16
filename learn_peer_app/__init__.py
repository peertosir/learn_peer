from flask import Flask, render_template
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
login_manager.login_view = 'core.join_us'
###
from learn_peer_app.models import User, Lecture, Task, Course
from learn_peer_app.users.views import users
from learn_peer_app.core.views import core
from learn_peer_app.courses.views import courses
from learn_peer_app.tasks.views import tasks
from learn_peer_app.lectures.views import lectures
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(courses)
app.register_blueprint(tasks)
app.register_blueprint(lectures)


#Error handlers
@app.errorhandler(403)
def not_allowed_error(error):
    return render_template('errors/404.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/html'), 500