from flask import render_template, redirect, Blueprint, url_for, request, abort
from learn_peer_app.courses.forms import CourseForm
from learn_peer_app.models import User, Course, Lecture, Task, course_students_maps
from flask_login import login_required, current_user
from learn_peer_app import db

courses = Blueprint('courses', __name__, url_prefix='/courses')

@courses.route('/create', methods=['POST', 'GET'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(title=form.title.data, description=form.description.data,
                        max_participants=form.max_participants.data, date_start=form.date_start.data,
                        date_finish=form.date_finish.data, mentor_id=current_user.id)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('course.index'))
    return render_template('courses/create.html', form=form)


@courses.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_course(id):
    course = Course.query.get_or_404(id)
    form = CourseForm()
    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.description.data
        course.date_start = form.date_start.data
        course.date_finish = form.date_finish.data
        course.max_participants = form.max_participants.data
        db.session.commit()
        return redirect(url_for('core.index'))
    if request.method == 'GET':
        form.title.data = course.title
        form.description.data = course.description
        form.max_participants.data = course.max_participants
        form.date_start.data = course.date_start
        form.date_finish.data = course.date_finish
    return render_template('courses/update.html', form=form)


@courses.route('/delete/<int:id>')
@login_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    if current_user.id != course.mentor_id:
        abort(403)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('core.index'))


@courses.route('/<int:id>')
@login_required
def get_course(id):
    course = Course.query.get_or_404(id)
    if current_user.status == "Student":
        can_sign_up = True if course not in current_user.courses_part else False
    else:
        can_sign_up = False
    count_participants = len(course.course_students)
    lectures = course.lectures
    return render_template('courses/course.html', course=course, amount=count_participants, lectures=lectures,
                           can_sign_up=can_sign_up)


@courses.route('/all_courses')
@login_required
def get_all_list():
    if current_user.status == "Teacher":
        courses = Course.query.filter(Course.mentor_id != current_user.id).all()
    else:
        subq = Course.query.join(
            Course.course_students
        ).filter(
            current_user.id == User.id
        ).all()
        excluded = [i.id for i in subq]
        courses = Course.query.filter(Course.id.notin_(excluded))
    return render_template("courses/get_all_list.html", courses=courses)


@courses.route('/your_courses')
@login_required
def get_my_list():
    if current_user.status == "Teacher":
        courses = Course.query.filter(Course.mentor_id == current_user.id).all()
    else:
        courses = Course.query.join(
            Course.course_students
        ).filter(
            current_user.id == User.id
        ).all()
    return render_template("courses/get_my_list.html", courses=courses)


@courses.route('/join_course/<int:id>')
@login_required
def join_course(id):
    course = Course.query.get(id)
    course.course_students.append(current_user)
    db.session.commit()
    return redirect(url_for('courses.get_course', id=course.id))

