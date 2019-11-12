from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField("Task title: ", validators=[DataRequired()])
    description = TextAreaField("Task description: ", validators=[DataRequired()])
    executor = SelectField("Choose assignee for task: ", coerce=int)
    submit = SubmitField("Go")

