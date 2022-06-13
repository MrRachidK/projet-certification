import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask
from credentials import sql_user, sql_password, sql_host, sql_database
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.config.from_object('config')

app.config['MYSQL_USER'] = sql_user
app.config['MYSQL_PASSWORD'] = sql_password
app.config['MYSQL_HOST'] = sql_host
app.config['MYSQL_DATABASE'] = sql_database

mysql = MySQL(app)

from pokemon_app import views
from pokemon_app import db

@app.cli.command("init_db")
def init_db():
    db.init_db(mysql)