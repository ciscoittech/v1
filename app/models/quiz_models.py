from mongoengine import Document, StringField, ListField, ReferenceField
import mongoengine

class Vendor(Document):
    name = StringField(required=True, unique=True)
    exams = ListField(ReferenceField('Exam'))

class Exam(Document):
    vendor = ReferenceField(Vendor, reverse_delete_rule=mongoengine.CASCADE)
    title = StringField(required=True)
    description = StringField()
    subsections = ListField(ReferenceField('Subsection'))

class Subsection(Document):
    exam = ReferenceField(Exam, reverse_delete_rule=mongoengine.CASCADE)
    title = StringField(required=True)
    description = StringField()
    questions = ListField(ReferenceField('Question'))

class Question(Document):
    subsection = ReferenceField(Subsection, reverse_delete_rule=mongoengine.CASCADE)
    content = StringField(required=True)
    # You can add more fields like options, correct answer, etc.