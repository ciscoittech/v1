# app/forms/resume_forms.py

from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired, URL

class ResumeUploadForm(FlaskForm):
    resume = FileField('Upload Resume', validators=[DataRequired()])
    job_link = StringField('Job Link', validators=[DataRequired(), URL()])
    submit = SubmitField('Process')
