import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
from flask import Flask
from pokemon_app import app
import pandas as pd
from src.features.functions import create_dictionaries
import mysql.connector

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(pokemon_id, photo, mysql, cursor):
    print("Inserting BLOB into images table")
    try:
        cursor = cursor

        sql_insert_blob_query = """ INSERT INTO images
                          (Number, Image) VALUES (%s,%s)"""

        pokemonPicture = convertToBinaryData(photo)

        # Convert data into tuple format
        insert_blob_tuple = (pokemon_id, pokemonPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        mysql.connection.commit()
        print("Image and file inserted successfully as a BLOB into images table", result)
    
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

### Initialize MySQL database
def init_db(mysql):
    pokemon_data = pd.read_csv(os.path.join(basedir, 'data/intermediate/pokemon.csv'), index_col=False, delimiter = ',')
    """ combats_data = pd.read_csv(os.path.join(basedir, 'data/raw/combats.csv'), index_col=False, delimiter = ',') """
    cursor = mysql.connection.cursor()
    # Executing SQL Statements

    ## Database
    cursor.execute("DROP DATABASE IF EXISTS pokemon_analytics")
    cursor.execute("CREATE DATABASE IF NOT EXISTS pokemon_analytics")
    cursor.execute("USE pokemon_analytics")

    ## Tables
    ### Pokemon
    cursor.execute('''DROP TABLE IF EXISTS pokemon''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemon (
        Number INT NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Type_1 VARCHAR(255) NOT NULL,
        Type_2 VARCHAR(255) NOT NULL,
        HP INT NOT NULL,
        Attack INT NOT NULL,
        Defense INT NOT NULL,
        Sp_Atk INT NOT NULL,
        Sp_Def INT NOT NULL,
        Speed INT NOT NULL,
        Generation INT NOT NULL,
        Legendary TINYINT NOT NULL,
        PRIMARY KEY (Number)
    ) 
    ''')

    ### Duels
    cursor.execute('''DROP TABLE IF EXISTS combats''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS combats (
        ID INT NOT NULL AUTO_INCREMENT,
        First_pokemon INT NOT NULL,
        Second_pokemon INT NOT NULL,
        Winner INT NOT NULL,
        PRIMARY KEY (ID),
        FOREIGN KEY (First_pokemon) REFERENCES pokemon(Number),
        FOREIGN KEY (Second_pokemon) REFERENCES pokemon(Number),
        FOREIGN KEY (Winner) REFERENCES pokemon(Number)
    )
    ''')

    ### Images
    cursor.execute('''DROP TABLE IF EXISTS images''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        Number INT NOT NULL AUTO_INCREMENT,
        Image BLOB NOT NULL,
        PRIMARY KEY (Number),
        FOREIGN KEY (Number) REFERENCES pokemon(Number)
    )
    ''')

    ### Users
    cursor.execute('''DROP TABLE IF EXISTS users''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        ID INT NOT NULL AUTO_INCREMENT,
        Last_Name VARCHAR(255) NOT NULL,
        First_Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        PRIMARY KEY (ID)
    )
    ''')

    # Insertion of data
    for i, row in pokemon_data.iterrows():
        sql = "INSERT INTO pokemon VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, tuple(row))

    for i in range(1, 801):
        insertBLOB(i, os.path.join(basedir, 'data/raw/images/{}.png'.format(i)), mysql, cursor)
        

    """ for i, row in combats_data.iterrows():
        sql = "INSERT INTO combats (First_pokemon, Second_pokemon, Winner) VALUES (%s, %s, %s)"
        cursor.execute(sql, tuple(row)) """
    
    """ cursor.execute('''
    SELECT 
        c.ID, 
        p.Name as 'First Pokemon', 
        p1.Name as 'Second Pokemon',
        p2.Name as 'Winner'
    FROM `combats` c
    JOIN `pokemon` p on p.Number = c.First_pokemon
    JOIN `pokemon` p1 on p1.Number = c.Second_pokemon
    JOIN `pokemon` p2 on p2.Number = c.Winner
    ''') """
    
    
    # Saving the Actions performed on the DB
    mysql.connection.commit()
    
    # Closing the cursor
    cursor.close()

def get_mapped_data(mysql):
    cursor = mysql.connection.cursor()
    # Executing SQL Statements
    cursor.execute("USE pokemon_analytics")
    pokemon_data = pd.read_sql('''SELECT * FROM pokemon''', con=mysql.connection)
    name_dict, type_dict, stats_dict = create_dictionaries(pokemon_data)
    cursor.close()

    return name_dict, type_dict, stats_dict

