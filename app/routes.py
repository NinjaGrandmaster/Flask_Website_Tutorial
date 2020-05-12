from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Robert'}
    posts = [
        {
            'author': {'username': 'General Kenobi'},
            'body': 'Hello There!'
        },
        {
            'author': {'username': 'General Grievous'},
            'body': 'General Kenobi. You are a bold one.'
        }
    ]
    # return render_template('index.html', user=user)
    return render_template('index.html', title='Home', posts=posts)


# GET - requests that return information to the client
# POST - requests are typically used when the browser submits form data to the server
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in redirect them to main page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # load user from the database
        user = User.query.filter_by(username=form.username.data).first()
        # check if user is valid
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # login the user
        login_user(user, remember=form.remember_me.data)

        # If the login URL does not have a next argument, then the user is redirected to the index page.
        # If the login URL includes a next argument that is set to a relative path (or in other words, a URL without
        # the domain portion), then the user is redirected to that URL.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        # If the login URL includes a next argument that is set to a full URL that includes a domain name, then the
        # user is redirected to the index page.
        return redirect(next_page)

    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        '''
        exist = user.username
        if exist:
            flash('Username already exists')
            return redirect(url_for('register'))
        '''
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
