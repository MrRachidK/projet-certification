from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from pokemon_app.models import User, db, init_db

auth = Blueprint('auth', __name__)

@auth.before_app_first_request
def load_data():
    init_db()

@auth.route('/', methods=['GET'])
def goto_login():
    return redirect(url_for('auth.login'))

# Login

@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/login', methods =['POST'])
def login_post():

    current_app.logger.info("Login attempt", extra={"page": "login"})

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.find_by_email(email)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'alert')
        current_app.logger.warning("Login failed", extra = {'page':'login'})
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    flash("Login Successful !! Welcome to Pokemon Arena, " + user.username + " !", "alert")

    return redirect(url_for('main.home'))

# Logout

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Sign Up

@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods =['POST'])
def signup_post():
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.find_by_email(email) # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists', 'alert')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(last_name=last_name, first_name=first_name, email=email, username=username, password=generate_password_hash(password, method='sha256'), role='user')

    # add the new user to the database
    new_user.save_to_db()

    return redirect(url_for('auth.login'))
