import sys 
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
import pandas as pd

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
    cursor.execute("DROP DATABASE IF EXISTS pokemon_relationals")
    cursor.execute("CREATE DATABASE IF NOT EXISTS pokemon_relationals")
    cursor.execute("USE pokemon_relationals")

    ## Tables
    ### Pokemon
    cursor.execute('''DROP TABLE IF EXISTS pokemon''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemon (
        number INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        type_1 VARCHAR(255) NOT NULL,
        type_2 VARCHAR(255) NOT NULL,
        hp INT NOT NULL,
        attack INT NOT NULL,
        defense INT NOT NULL,
        sp_atk INT NOT NULL,
        sp_def INT NOT NULL,
        speed INT NOT NULL,
        generation INT NOT NULL,
        legendary TINYINT NOT NULL,
        PRIMARY KEY (number)
    ) 
    ''')

    ### Duels
    cursor.execute('''DROP TABLE IF EXISTS combats''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS combats (
        id INT NOT NULL AUTO_INCREMENT,
        first_pokemon INT NOT NULL,
        second_pokemon INT NOT NULL,
        winner INT NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (first_pokemon) REFERENCES pokemon(number),
        FOREIGN KEY (second_pokemon) REFERENCES pokemon(number),
        FOREIGN KEY (winner) REFERENCES pokemon(number)
    )
    ''')

    ### Images
    cursor.execute('''DROP TABLE IF EXISTS images''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        number INT NOT NULL AUTO_INCREMENT,
        image BLOB NOT NULL,
        PRIMARY KEY (number),
        FOREIGN KEY (number) REFERENCES pokemon(number)
    )
    ''')

    ### Users
    cursor.execute('''DROP TABLE IF EXISTS users''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT NOT NULL AUTO_INCREMENT,
        last_name VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
    )
    ''')

    # Insertion of data
    for i, row in pokemon_data.iterrows():
        sql = "INSERT INTO pokemon VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, tuple(row))

    for i in range(1, 801):
        insertBLOB(i, os.path.join(basedir, 'data/raw/images/{}.png'.format(i)), mysql, cursor)
        

    """ for i, row in combats_data.iterrows():
        sql = "INSERT INTO combats (first_pokemon, second_pokemon, winner) VALUES (%s, %s, %s)"
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

def create_dictionaries(data):
    name_df = data.iloc[:, 0:2]
    name_dict = name_df.set_index('number').to_dict()['name']

    type_df = data.iloc[:, 0:4]
    type_df = type_df.drop('name', axis=1)
    type_dict = type_df.set_index('number').T.to_dict('list')

    stats_df = data.drop(['type_1', 'type_2', 'name', 'generation'], axis=1)
    stats_dict = stats_df.set_index('number').T.to_dict('list')

    return name_dict, type_dict, stats_dict

def get_mapped_data(mysql):
    cursor = mysql.connection.cursor()
    # Executing SQL Statements
    cursor.execute("USE pokemon_relationals")
    pokemon_data = pd.read_sql('''SELECT * FROM pokemon''', con=mysql.connection)
    name_dict, type_dict, stats_dict = create_dictionaries(pokemon_data)
    cursor.close()

    return name_dict, type_dict, stats_dict
