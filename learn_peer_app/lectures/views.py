from flask import render_template, redirect, Blueprint, url_for, request, abort
from learn_peer_app.lectures.forms import LectureForm
from learn_peer_app.models import User, Course, Lecture, Task
from flask_login import login_required, current_user
from learn_peer_app import db

lectures = Blueprint('lectures', __name__, url_prefix='/lectures')

@lectures.route('/create', methods=['POST', 'GET'])
@login_required
def create_lecture():
    form = LectureForm()
    form_courses_list = [(i.id, i.title) for i in Course.query.filter_by(mentor_id=current_user.id).all()] \
        if Course.query.filter_by(mentor_id=current_user.id).all() else []
    form.course.choices = form_courses_list
    if form.validate_on_submit():
        lecture = Lecture(title=form.title.data, content=form.content.data,
                    author_id=current_user.id, course_id=form.course.data)
        db.session.add(lecture)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('lectures/create.html', form=form, choices=form_courses_list)


@lectures.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_lecture(id):
    lecture = Lecture.query.get_or_404(id)
    form = LectureForm()
    form_courses_list = [(i.id, i.title) for i in Course.query.filter_by(mentor_id=current_user.id).all()] \
        if Course.query.filter_by(mentor_id=current_user.id).all() else []
    form.course.choices = form_courses_list
    if form.validate_on_submit():
        lecture.title = form.title.data
        lecture.content = form.content.data
        lecture.course_id = form.course.data
        db.session.commit()
        return redirect(url_for('core.index'))
    if request.method == 'GET':
        form.title.data = lecture.title
        form.content.data = lecture.content
        form.course.data = lecture.course_id
    return render_template('lectures/update.html', form=form, choices=form_courses_list)


@lectures.route('/delete/<int:id>')
@login_required
def delete_lecture(id):
    lecture = Lecture.query.get_or_404(id)
    if current_user.id != lecture.author_id:
        abort(403)
    db.session.delete(lecture)
    db.session.commit()
    return redirect(url_for('core.index'))


@lectures.route('/<int:id>')
@login_required
def get_lecture(id):
    lecture = Lecture.query.get_or_404(id)
    tasks = lecture.tasks
    return render_template('lectures/lecture.html', lecture=lecture, tasks=tasks)