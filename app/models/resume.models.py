# app/models/resume_models.py

from mongoengine import Document, StringField, FileField, ReferenceField, URLField

from app.models.user_models import User

class Resume(Document):
    user = ReferenceField(User)
    original_resume = FileField()
    transformed_resume = FileField()
    job_link = URLField()
