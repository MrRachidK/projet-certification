import sys 
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
import logging as lg

db = SQLAlchemy()

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type_1 = db.Column(db.String(255))
    type_2 = db.Column(db.String(255))
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    sp_atk = db.Column(db.Integer)
    sp_def = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    generation = db.Column(db.Integer)
    legendary = db.Column(db.Boolean)
    
    def __repr__(self):
        return '<Pokemon %r>' % self.name

    def pokemon_json(self):
        return {
            'number': self.number,
            'name': self.name,
            'type_1': self.type_1,
            'type_2': self.type_2,
            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'sp_atk': self.sp_atk,
            'sp_def': self.sp_def,
            'speed': self.speed,
            'generation': self.generation,
            'legendary': self.legendary,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Combat(db.Model):
    __tablename__ = 'combats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    first_pokemon = db.Column(db.String(255), ForeignKey('pokemon.number'))
    second_pokemon = db.Column(db.String(255), ForeignKey('pokemon.number'))
    winner = db.Column(db.String(255), ForeignKey('pokemon.number'))

    def __repr__(self):
        return '<Combat %r>' % self.id

    def combat_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_pokemon': self.first_pokemon,
            'second_pokemon': self.second_pokemon,
            'winner': self.winner,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Image(db.Model):
    __tablename__ = 'images'
    number = db.Column(db.Integer, ForeignKey('pokemon.number'), primary_key=True)
    image = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<Image %r>' % self.number

    def image_json(self):
        return {
            'number': self.number,
            'image': self.image
        }

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(255), )
    first_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __repr__(self):
        return '<User %r>' % self.username

    def user_json(self):
        return {'last_name': self.last_name,
                'first_name': self.first_name, 
                'email': self.email,
                'username': self.username,
                }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

def init_db():
    db.drop_all()
    db.create_all()

    pokemon_data = pd.read_csv(os.path.join(basedir, 'data/intermediate/pokemon.csv'), index_col=False, delimiter = ',')
    pokemon_data = pokemon_data.rename(columns={'Sp. Atk': 'sp_atk', 'Sp. Def': 'sp_def'})
    pokemon_data.to_sql('pokemon', db.engine, if_exists='append', index=False)    

    for i in range(1, 801):
        image = convertToBinaryData(os.path.join(basedir, 'data/raw/images/{}.png'.format(i)))
        image_db = Image(number=i, image=image)
        image_db.save_to_db()

    lg.info('Database initialized')

def create_dictionaries(data):
    name_df = data.iloc[:, 0:2]
    name_dict = name_df.set_index('number').to_dict()['name']

    type_df = data.iloc[:, 0:4]
    type_df = type_df.drop('name', axis=1)
    type_dict = type_df.set_index('number').T.to_dict('list')

    stats_df = data.drop(['type_1', 'type_2', 'name', 'generation'], axis=1)
    stats_dict = stats_df.set_index('number').T.to_dict('list')

    return name_dict, type_dict, stats_dict

def get_mapped_data():
    data = db.session.query(Pokemon).all()
    df = pd.DataFrame([p.pokemon_json() for p in data])
    name_dict, type_dict, stats_dict = create_dictionaries(df)

    return name_dict, type_dict, stats_dict

def get_combat_data(user_id):
    data = db.session.query(Combat).all()
    df = [c.combat_json() for c in data]
    df = [c for c in df if c['user_id'] == user_id]

    return df

if __name__ == '__main__':
    init_db()
    