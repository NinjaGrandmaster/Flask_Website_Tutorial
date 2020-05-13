from flask import Flask
# "config" is the name of the Python module config.py, and obviously the one with the uppercase "C" is the actual class.
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # initialize database
migrate = Migrate(app, db)  # initialize migration engine
# function that handles logins
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors
