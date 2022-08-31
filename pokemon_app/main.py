from mimetypes import init
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
import json
import requests

from pokemon_app.models import db, Combat, User, get_mapped_data, get_combat_data, get_user_data, init_db

main = Blueprint('main', __name__)

"""@main.before_app_first_request
def load_data():
    init_db()"""

## Views

# Home page

@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # Get mapped data
    name_dict, type_dict, stats_dict = get_mapped_data()

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
            url = "https://api-pokemon-arena.azurewebsites.net/get_prediction"
            prediction = requests.get(url, json=pokemon_json).text

            # Get index of prediction from name_dict
            keys = list(name_dict.keys())
            values = list(name_dict.values())
            prediction_index = keys[values.index(prediction)]

            new_duel = Combat(user_id = current_user.id, first_pokemon=pokemon_data['first_pokemon'], second_pokemon=int(pokemon_data['second_pokemon']), winner=prediction_index)
            new_duel.save_to_db()
        
            return redirect(url_for('main.result', pokemon_json = pokemon_json, prediction_text = prediction, prediction_index = prediction_index))
    else:
        prediction = ""

    return render_template("home.html", pokemon_name = name_dict, pokemon_stats = stats_dict, pokemon_types = type_dict)

# Result page

@main.route('/result', methods=['GET'])
@login_required
def result():
    # Get pokemon data as a dictionary
    pokemon_data = request.args.get('pokemon_json')
    pokemon_data = json.loads(pokemon_data)
    prediction_text = request.args.get('prediction_text')
    prediction_index = request.args.get('prediction_index', type=int)
    
    # Get mapped results
    name_dict, type_dict, stats_dict = get_mapped_data()
    pokemon_name = name_dict 
    pokemon_stats = stats_dict 
    pokemon_types = type_dict
    return render_template('result.html', pokemon_data = pokemon_data, prediction_text = prediction_text, prediction_index = prediction_index, pokemon_name = pokemon_name, pokemon_stats = pokemon_stats, pokemon_types = pokemon_types)


# Profile

@main.route('/profile')
@login_required
def profile():
    # Get mapped data
    name_dict, type_dict, stats_dict = get_mapped_data()

    # Get combats data
    combats = get_combat_data(current_user.id)
    
    return render_template("profile.html", combats = combats, name_dict = name_dict, last_name=current_user.last_name, first_name=current_user.first_name, username=current_user.username, email=current_user.email)

# Admin

@main.route('/admin')
@login_required
def admin():
    if current_user.role == "admin":
        # Get all the users in the database
        users = get_user_data()
        return render_template("admin.html", users = users)

    flash("You don't have permission to access this resource", "alert")
    return redirect(url_for("main.home"))
    
@main.route('/admin/update_user', methods=['GET'])
@login_required
def update_user():
    if current_user.role == "admin":
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)
        return render_template("update_user.html", user = user)

    flash("You don't have permission to access this resource", "alert")
    return redirect(url_for("main.home"))

@main.route('/admin/update_user', methods=['POST'])
@login_required
def update_user_post():
    if current_user.role == "admin":
        # Get the user id
        user_id = request.args.get('user_id')
        # Get the user data
        user = User.find_by_id(user_id)
        # Get the user data from the form
        user.last_name = request.form.get("last_name")
        user.first_name = request.form.get("first_name")
        user.email = request.form.get("email")
        user.username = request.form.get("username")

        user.save_to_db()

        flash("User updated successfully !")

        return redirect(url_for("main.admin"))

    flash("You don't have permission to access this resource", "alert")
    return redirect(url_for("main.home"))

@main.route('/admin/delete_user', methods=['GET'])
@login_required
def delete_user():
    if current_user.role == "admin":
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)

        return render_template("delete_user.html", user = user)

    flash("You don't have permission to access this resource", "alert")
    return redirect(url_for("main.home"))

@main.route('/admin/delete_user', methods=['POST'])
@login_required
def delete_user_post():
    if current_user.role == "admin":
        # Get the user id
        user_id = request.args.get('user_id')
        # Get the user data
        user = User.find_by_id(user_id)
        # Delete the user
        user.delete_from_db()

        flash("User deleted successfully !")

        return redirect(url_for("main.admin"))

    flash("You don't have permission to access this resource", "alert")
    return redirect(url_for("main.home"))