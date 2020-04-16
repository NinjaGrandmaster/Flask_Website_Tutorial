import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # get datebase url from environment variables
    # as fallback configure database app.db in application main directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATA_BASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Disable signal that signals application every time a database change is made
    SQLALCHEMY_TRACK_MODIFICATIONS = False
