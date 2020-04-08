from flask import Flask
# "config" is the name of the Python module config.py, and obviously the one with the uppercase "C" is the actual class.
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
