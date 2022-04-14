from flask import Flask
from credentials import sql_user, sql_password, sql_host
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_object('config')

app.config['MYSQL_USER'] = sql_user
app.config['MYSQL_PASSWORD'] = sql_password
app.config['MYSQL_DB'] = 'products'
app.config['MYSQL_HOST'] = sql_host

mysql = MySQL(app)

from products_app import views
from products_app import db

@app.cli.command("init_db")
def init_db():
    db.init_db(mysql)