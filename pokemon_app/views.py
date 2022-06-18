from distutils.command.build_scripts import first_line_re
import email
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request, json
import ast
import requests

from pokemon_app import app, db
from pokemon_app.__init__ import mysql

## Views

# Login

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
        return "User not found"
    else:
        if check_password_hash(data[5], password):
            return "Login successful"
        else:
            return "Incorrect password"

# Sign Up

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
    cursor.execute("INSERT INTO users (last_name, first_name, email, username, password) VALUES (%s, %s, %s, %s, %s)", (last_name, first_name, email, username, hashed_password))
    mysql.connection.commit()
    cursor.close()

    return "Signup successful"

# Home page

@app.route('/', methods=['GET', 'POST'])
def home():
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

    
    return render_template("index.html", pokemon_name = name_dict, pokemon_stats = stats_dict, pokemon_types = type_dict, prediction_text = prediction)
