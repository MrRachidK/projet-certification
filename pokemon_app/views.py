import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import requests
import re

from pokemon_app import app, db
from pokemon_app.__init__ import mysql

## Views

# Home page

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'loggedin' in session :
        # Get mapped data
        name_dict, type_dict, stats_dict = db.get_mapped_data(mysql)  

        # Get values through input bars
        pokemon_1 = request.form.get("first_pokemon")
        pokemon_2 = request.form.get("second_pokemon")
        data = {'first_pokemon': pokemon_1, 'second_pokemon': pokemon_2}
        pokemon_json = json.dumps(data)

        # If a form is submitted
        if request.method == "POST":
            
            # Get prediction
            url = "http://localhost:5001/get_prediction"
            prediction = requests.get(url, json=pokemon_json).text
            print(prediction)
            
        else:
            prediction = ""
        
        return render_template("home.html", pokemon_name = name_dict, pokemon_stats = stats_dict, pokemon_types = type_dict, prediction_text = prediction)

    return redirect(url_for('login'))

# Login / Logout
"""
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute('USE pokemon_relationals')
    cursor.execute("SELECT * FROM users WHERE email = %s", [email])
    data = cursor.fetchone()
    cursor.close()

    if data is None:
        return redirect(url_for('login'))
    else:
        if check_password_hash(data[5], password):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

@app.route('/private')
@login_required
def private():
    return f"Bonjour {current_user.name}"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
"""

@app.route('/', methods =['GET', 'POST'])
def login():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('USE pokemon_relationals')
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))

# Sign Up
"""
@app.route('/signup')
def signup():
    return render_template('signup.html')
    
@app.route('/signup', methods=['POST'])
def signup_post():
    last_name = request.form['last_name']
    first_name = request.form['first_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    cursor = mysql.connection.cursor()
    cursor.execute('USE pokemon_relationals')

    cursor.execute("SELECT * FROM users WHERE email = %s", [email])
    data = cursor.fetchone()

    if data is None:
        cursor.execute("INSERT INTO users (last_name, first_name, email, username, password) VALUES (%s, %s, %s, %s, %s)", (last_name, first_name, email, username, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))

    else:
        return redirect(url_for('signup'))
"""
@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('USE pokemon_relationals')
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s)', (last_name, first_name, email, username, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('signup.html', msg = msg)

# Profile

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor()
        cursor.execute('USE pokemon_relationals')
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))