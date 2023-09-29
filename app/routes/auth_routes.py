from flask import render_template, redirect, url_for, flash, request, Blueprint, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models.user_models import User
from app.forms.auth_forms import LoginForm, RegistrationForm
from app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')


@app.route('/tables', methods=['GET', 'POST'])
def tables():
    return render_template('home/tables.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user_by_username = User.objects(username=form.username.data).first()
        if existing_user_by_username:
            flash('That username is already taken. Please choose a different one.', 'danger')
            return render_template('accounts/register.html', title='Register', form=form)

        # Check if email already exists
        existing_user_by_email = User.objects(email=form.email.data).first()
        if existing_user_by_email:
            flash('That email is already registered. Please log in or use a different email.', 'danger')
            return render_template('accounts/register.html', title='Register', form=form)

        # If both checks pass, create the user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        flash('Registration successful!', 'success')
        return redirect(url_for('profile'))
    return render_template('accounts/register.html', title='Register', form=form)



@app.route('/success', methods=['GET', 'POST'])
def success():
    return "success"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home/index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('profile')
        return redirect(next_page)

    return render_template('accounts/login.html', title='Sign In', form=form)


from flask_login import logout_user

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))