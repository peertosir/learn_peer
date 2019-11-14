from learn_peer_app import app
from flask import render_template, Blueprint
from flask_login import login_required
from learn_peer_app import db
from learn_peer_app.models import User

core = Blueprint('core', __name__)


@core.route('/')
@login_required
def index():
    #TO-DO
    return render_template('index.html')

@core.route('/join_us')
def join_us():
    return render_template('without_login.html')


@core.route('/students')
@login_required
def get_students():
    students = User.query.filter(User.status=="Student").all()
    return render_template("students.html", students=students)


@core.route('/teachers')
@login_required
def get_teachers():
    teachers = User.query.filter(User.status=="Teacher").all()
    return render_template("teachers.html", teachers=teachers)

