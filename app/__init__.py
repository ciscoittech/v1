from flask import Flask
from flask_login import LoginManager
import mongoengine as me

from app.models.user_models import User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Connect to the MongoDB database using mongoengine
me.connect('quicksilver', host='localhost', port=27017)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  #


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except me.DoesNotExist:
        return None


# Import routes after creating the app instance
from app.routes import auth_routes, user_routes, quiz_routes
