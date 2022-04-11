import sys
sys.path.insert(0, '/home/apprenant/Documents/projet-certification/')
import os
from config import basedir
from flask import Flask, render_template, request
import pandas as pd
import joblib
from products_app import app

@app.route('/', methods=['GET', 'POST'])
def main():
    
    # If a form is submitted
    if request.method == "POST":
        
        # Unpickle classifier
        clf = joblib.load(os.path.join(basedir, 'src/clf.pkl'))
        
        # Get values through input bars
        height = request.form.get("height")
        weight = request.form.get("weight")
        
        # Put inputs to dataframe
        X = pd.DataFrame([[height, weight]], columns = ["Height", "Weight"])
        
        # Get prediction
        prediction = clf.predict(X)[0]
        
    else:
        prediction = ""
        
    return render_template("index.html", prediction_text = prediction)
