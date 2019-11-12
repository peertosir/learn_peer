from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class CourseForm(FlaskForm):
    title = StringField("Course title: ", validators=[DataRequired()])
    description = StringField("Brief description: ", validators=[DataRequired()])
    date_start = DateField("Date and time of the start: ", validators=[DataRequired()])
    date_finish = DateField("Date and time of the finish: ", validators=[DataRequired()])
    max_participants = IntegerField("Max participants: ", validators=[DataRequired()])
    submit = SubmitField("Go")

