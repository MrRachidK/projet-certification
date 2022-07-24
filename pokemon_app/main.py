from distutils.command.build_scripts import first_line_re
from hashlib import new
import sys
import os
from turtle import st
from unicodedata import name

from pokemon_app.auth import login
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
from flask import render_template, request, redirect, url_for, session, Blueprint, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import requests

from pokemon_app import db
from .utils import admin_required

main = Blueprint('main', __name__)

## Views

# Home page

@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # Get mapped data
    name_dict, type_dict, stats_dict = db.get_mapped_data()

    # Get values through input bars
    pokemon_1 = request.form.get("first_pokemon")
    pokemon_2 = request.form.get("second_pokemon")
    pokemon_data = {'first_pokemon': pokemon_1, 'second_pokemon': pokemon_2}
    pokemon_json = json.dumps(pokemon_data)

    # If a form is submitted
    if request.method == "POST":
        if pokemon_data['first_pokemon'] == pokemon_data['second_pokemon']:
            flash("Please choose two different Pokemon !")    
            return redirect(url_for("main.home"))
        else :
        # Get prediction
            url = "http://localhost:5001/get_prediction"
            prediction = requests.get(url, json=pokemon_json).text
            new_duel = db.Combat(user_id = current_user.id, first_pokemon=name_dict[int(pokemon_data['first_pokemon'])], second_pokemon=name_dict[int(pokemon_data['second_pokemon'])], winner=prediction)
            new_duel.save_to_db()
        
            return render_template('result.html', pokemon_name = name_dict, pokemon_stats = stats_dict, pokemon_types = type_dict, pokemon_data = pokemon_data, prediction_text = prediction)
    else:
        prediction = ""

    return render_template("home.html", pokemon_name = name_dict, pokemon_stats = stats_dict, pokemon_types = type_dict)


# Profile

@main.route('/profile')
@login_required
def profile():
    # Get combats data
    combats = db.get_combat_data(current_user.id)
    
    return render_template("profile.html", combats = combats, last_name=current_user.last_name, first_name=current_user.first_name, username=current_user.username, email=current_user.email)

# Admin

@main.route('/admin')
@admin_required
@login_required
def admin():
    return render_template("admin.html")
