from flask import Flask
from products_app import app
import pandas as pd

def init_db(mysql):
    data = pd.read_csv('/home/apprenant/Documents/projet-certification/data/data.csv', index_col=False, delimiter = ',')
    cursor = mysql.connection.cursor()
    #Executing SQL Statements
    cursor.execute('''DROP TABLE animals''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS animals (
        height FLOAT NOT NULL,
        weight FLOAT NOT NULL,
        species VARCHAR(255) NOT NULL
    ) ''')

    for i,row in data.iterrows():
        sql = "INSERT INTO animals VALUES (%s,%s,%s)"
        cursor.execute(sql, tuple(row))
    
    #Saving the Actions performed on the DB
    mysql.connection.commit()
    
    #Closing the cursor
    cursor.close()
