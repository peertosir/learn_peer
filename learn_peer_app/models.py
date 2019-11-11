from learn_peer_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

course_students_maps = db.Table(
    'course_students_maps',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    skype = db.Column(db.String(40))
    reg_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    courses_mentor = db.relationship('Course', backref='course_mentor', lazy='dynamic')
    courses_part = db.relationship('Course', secondary=course_students_maps,
                                   backref='course_students', lazy='dynamic')
    lecture_author = db.relationship('Lecture', backref='lecture_author', lazy='dynamic')

    def __init__(self, username, email, password, status, phone='', skype=""):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.status = status
        self.phone = phone
        self.skype = skype

    def __repr__(self):
        return f"User: {self.username}, status: {self.status}"

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date_start = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    date_finish = db.Column(db.DateTime, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    lectures = db.relationship('Lecture', backref='course')

    def __init__(self, title, description, mentor_id, max_participants):
        self.title = title
        self.description = description
        self.max_participants = max_participants
        self.mentor_id = mentor_id

    def __repr__(self):
        return f"Course {self.title} by {self.course_mentor.username}"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Opened')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', foreign_keys=[author_id], backref='created_tasks')
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor = db.relationship('User', foreign_keys=[executor_id], backref='assigned_tasks')
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    lecture = db.relationship('Lecture', foreign_keys=[lecture_id], backref='linked_task')
    date_to_do = db.Column(db.DateTime)
    answer = db.Column(db.Text)

    def __init__(self, title, description, author_id, executor_id):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.executor_id = executor_id

    def __repr__(self):
        return f"Task from {self.author.username} for {self.executor.username}"



class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    tasks = db.relationship('Task', backref='to_lecture')
    date_to_happen = db.Column(db.DateTime)

    def __init__(self, title, content, author_id, course_id):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.course_id = course_id

    def __repr__(self):
        return f"Lecture {self.title} for course {self.course.title}"