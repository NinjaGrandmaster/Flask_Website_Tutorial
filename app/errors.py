from flask import render_template
from app import app, db


# Handel error code 404 HTTP errors
@app.errorhandler(404)
def not_fount_error(error):
    return render_template('404.html'), 404


# Handel error code 500 HTTP errors
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
