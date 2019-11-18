from flask import render_template, redirect, Blueprint, url_for, request, abort
from learn_peer_app.tasks.forms import TaskForm, ResolveTaskForm
from learn_peer_app.models import User, Course, Lecture, Task
from flask_login import login_required, current_user
from learn_peer_app import db

tasks = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks.route('/create/<int:lecture_id>', methods=['POST', 'GET'])
@login_required
def create_task(lecture_id):
    form = TaskForm()
    course_partic = Course.query.get(Lecture.query.get(lecture_id).course_id).course_students
    form_executors_list = [(i.id, i.username) for i in course_partic]
    form.executors.choices = form_executors_list
    if form.validate_on_submit():
        for executor in form.executors.data:
            task = Task(title=form.title.data, description=form.description.data,
                        author_id=current_user.id, executor_id=executor)
            task.lecture_id = lecture_id
            db.session.add(task)
        db.session.commit()
        return redirect(url_for('lectures.get_lecture', id=lecture_id))
    return render_template('tasks/create.html', form=form)


@tasks.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    form = TaskForm()
    course_partic = Course.query.get(Lecture.query.get(lecture_id).course_id).course_students
    form_executors_list = [(i.id, i.username) for i in course_partic]
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


@tasks.route('/assigned_tasks')
@login_required
def assigned_tasks():
    tasks = Task.query.filter(Task.executor_id == current_user.id)
    return render_template('tasks/todo_tasks.html', tasks=tasks)


@tasks.route('/get_assigned_task/<int:id>', methods=['POST', 'GET'])
@login_required
def get_assigned_task(id):
    task = Task.query.get(id)
    form = ResolveTaskForm()
    if form.validate_on_submit():
        task.answer = form.answer.data
        task.status = "Resolved"
        db.session.commit()
        return redirect(url_for('tasks.assigned_tasks'))
    return render_template('tasks/resolve_task.html', form=form, task=task)
