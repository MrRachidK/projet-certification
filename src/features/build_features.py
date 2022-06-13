# Import of the libraries
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import pandas as pd
from config import basedir
from src.features.functions import create_dictionaries, replace_things, calculate_stats, calculate_effectiveness

# Import of the data files

pokemon_data = pd.read_csv(os.path.join(basedir, 'data/intermediate/pokemon.csv'), index_col=False, delimiter = ',')
combats_data = pd.read_csv(os.path.join(basedir, 'data/raw/combats.csv'), index_col=False, delimiter = ',')

# Data processing

## Creation of columns

## Update of columns

#changing winner to 0 and 1, each corresponds to first and second pokemon respectively
combats_data.Winner[combats_data.Winner == combats_data.First_pokemon] = 0
combats_data.Winner[combats_data.Winner == combats_data.Second_pokemon] = 1

## Creation of dictionnaries

name_dict, type_dict, stats_dict = create_dictionaries(pokemon_data)

## Map the battle to pokemon's data

train_df = replace_things(combats_data, stats_dict, type_dict)
train_df = calculate_stats(train_df)
train_df = calculate_effectiveness(train_df)

train_df.to_csv(os.path.join(basedir, 'data/processed/train_df.csv'), index=False)