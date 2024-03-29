from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField("Task title: ", validators=[DataRequired()])
    description = TextAreaField("Task description: ", validators=[DataRequired()])
    executors = SelectMultipleField("Choose assignee for task: ", coerce=int)
    submit = SubmitField("Go")


class ResolveTaskForm(FlaskForm):
    answer = TextAreaField("Put your answer here")
    submit = SubmitField("Send to teacher")

