from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime


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


# Dynamic component, indicated as the <username> URL component that is surrounded by < and >. When a
# route has a dynamic component, Flask will accept any text in that portion of the URL, and will invoke the view
# function with the actual text as an argument. For example, if the client browser requests URL /user/susan, the view
# function is  going to be called with the argument username set to 'susan'.
@app.route('/user/<username>')
@login_required
def user(username):
    # first_or_404(), which works exactly like first() when there are results, but in the case that there are no
    # results automatically sends a 404 error back to the client. saves you checking if the query returned a user,
    # because when the username does not exist in the database the function will not return and instead a 404 exception
    # will be raised.
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    # If validate_on_submit() returns True, copy the data from the form into the user object and then write the object
    # to the database
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    # When the form is being requested for the first time with a GET request, pre-populate the fields with the data
    # that is stored in the database
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    # if validation error occurs request.method returns POST. But in the case of a validation error we do not want to
    # write anything to the form fields, because those were already populated by WTForms
    return render_template('edit_profile.html', title='Edit Profile', form=form)