from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    choices = RadioField('Choose an answer', choices=[], validators=[DataRequired()])
    submit_next = SubmitField('Submit & Next')
    submit_end = SubmitField('End Exam')