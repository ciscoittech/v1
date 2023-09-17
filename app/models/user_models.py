from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import mongoengine as me
from datetime import datetime


class User(UserMixin, me.Document):
    email = me.StringField(required=True, unique=True)
    username = me.StringField(required=True, unique=True)
    password_hash = me.StringField(required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


