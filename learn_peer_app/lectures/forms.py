from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class LectureForm(FlaskForm):
    title = StringField("Lecture title: ", validators=[DataRequired()])
    content = TextAreaField("Brief description: ", validators=[DataRequired()])
    course = SelectField("For which course? ", coerce=int)
    submit = SubmitField("Go")