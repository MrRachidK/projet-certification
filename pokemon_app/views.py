import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
from flask import render_template, request
from pokemon_app import app, db
from pokemon_app.__init__ import mysql

import urllib.request, json
import ast
import requests


@app.route('/', methods=['GET', 'POST'])
def main():
    # Get mapped data
    name_dict, type_dict, stats_dict = db.get_mapped_data(mysql)  

    # Get values through input bars
    pokemon_1 = request.form.get("First_Pokemon")
    pokemon_2 = request.form.get("Second_Pokemon")
    data = {'First_pokemon': pokemon_1, 'Second_pokemon': pokemon_2}
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
