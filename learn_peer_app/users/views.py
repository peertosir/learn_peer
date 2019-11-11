from flask import render_template, request, redirect, abort, url_for, Blueprint
from flask_login import login_required, login_user, logout_user
from learn_peer_app import db
from learn_peer_app.users.forms import LoginForm, RegisterForm
from learn_peer_app.models import User

users = Blueprint('users', __name__, url_prefix="/users")


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or next[0] == '/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('users/login.html', form=form)


@users.route('/register_teacher', methods=['POST', 'GET'])
def register_teacher():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, status="Teacher")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('users/register_teacher.html', form=form)


@users.route('/register_student', methods=['POST', 'GET'])
def register_student():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, status="Student")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('users/register_student.html', form=form)
