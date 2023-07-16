from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import os

SECRET_KEY = os.urandom(24)

application = Flask(__name__)
application.config.from_object(__name__)

application.config['UPLOAD_FOLDER'] = 'uploads'
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
application.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
application.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
application.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
application.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
application.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(application)

login_manager = LoginManager(application)
login_manager.login_view = 'login'

db = SQLAlchemy(application)