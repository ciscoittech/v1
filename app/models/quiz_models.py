from mongoengine import Document, StringField, ListField, ReferenceField
from datetime import datetime
import mongoengine as me

# class Vendor(Document):
#     name = StringField(required=True, unique=True)
#     exams = ListField(ReferenceField('Exam'))

# class Exam(Document):
#     vendor = ReferenceField(Vendor, reverse_delete_rule=mongoengine.CASCADE)
#     title = StringField(required=True)
#     description = StringField()
#     subsections = ListField(ReferenceField('Subsection'))

# class Subsection(Document):
#     exam = ReferenceField(Exam, reverse_delete_rule=mongoengine.CASCADE)
#     title = StringField(required=True)
#     description = StringField()
#     questions = ListField(ReferenceField('Question'))

# class Question(Document):
#     subsection = ReferenceField(Subsection, reverse_delete_rule=mongoengine.CASCADE)
#     content = StringField(required=True)
#     # You can add more fields like options, correct answer, etc.


class Quiz(me.Document):
    question_number = me.IntField(required=True)
    question = me.StringField(required=True)
    options = me.DictField()
    correct_answer = me.StringField(required=True)


class Question(me.Document):
    content = me.StringField(required=True)
    choices = me.DictField()
    correct_answer = me.StringField(required=True, choices=["A", "B", "C", "D", "E"])
    explanation = me.StringField()


class Subsection(me.Document):
    title = me.StringField(required=True)
    description = me.StringField()
    exam = me.ReferenceField('Exam')  # Reference to the Exam document
    questions = me.ListField(me.ReferenceField(Question))


class Exam(me.Document):
    name = me.StringField(required=True, unique=True)
    description = me.StringField()
    subsections = me.ListField(me.ReferenceField(Subsection))


class Result(me.Document):
    # user = me.ReferenceField(User, required=True)
    question = me.ReferenceField(Question, required=True)
    selected_answer = me.StringField(required=True)
    time_taken = me.StringField(required=True)  # Placeholder, make adjustments based on your needs
    is_correct = me.BooleanField(required=True)
    timestamp = me.DateTimeField(default=datetime.utcnow)
