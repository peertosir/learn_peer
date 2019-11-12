from flask import render_template, redirect, Blueprint, url_for, request, abort
from learn_peer_app.tasks.forms import TaskForm
from learn_peer_app.models import User, Course, Lecture, Task
from flask_login import login_required, current_user
from learn_peer_app import db

tasks = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks.route('/create', methods=['POST', 'GET'])
@login_required
def create_task():
    form = TaskForm()
    form_executors_list = [(i.id, i.username) for i in User.query.all()]
    form.executor.choices = form_executors_list
    print(form.validate())
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data,
                    author_id=current_user.id, executor_id=form.executor.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('core.index'))
    print("Kek")
    return render_template('tasks/create.html', form=form)


@tasks.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    form = TaskForm()
    form.executor.choices = [(i.id, i.username) for i in User.query.all()]
    print(form.validate())
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.executor_id = form.executor.data
        db.session.commit()
        return redirect(url_for('core.index'))
    if request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.executor.data = task.executor_id
    return render_template('tasks/update.html', form=form)


@tasks.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if current_user.id != task.author_id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('core.index'))


@tasks.route('/<int:id>')
@login_required
def get_task(id):
    task = Task.query.get_or_404(id)
    return render_template('tasks/task.html', task=task)