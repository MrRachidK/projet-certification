# Import of the libraries
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
import pandas as pd

# Import of the data files

pokemon_df = pd.read_csv(os.path.join(basedir, 'data/raw/pokemon.csv'))  # Pokemon Dataset
pokemon_df = pokemon_df.rename(index=str, columns={"#": "Number"})
pokemon_df = pokemon_df.rename(index=str, columns={"Type 1": "Type_1"})
pokemon_df = pokemon_df.rename(index=str, columns={"Type 2": "Type_2"})
combats_df = pd.read_csv(os.path.join(basedir, 'data/raw/combats.csv'))  # Combats Dataset
test_df = pd.read_csv(os.path.join(basedir, 'data/raw/tests.csv'))  # Test Dataset
prediction_df = test_df.copy() # Test Dataset copy

# Data cleaning

## Summary of the data

print("Shape of Pokemon dataset : " + str(pokemon_df.shape))
pokemon_df.info()
print(pokemon_df.describe())

print("Shape of Pokemon dataset : " + str(combats_df.shape))
combats_df.info()
print(combats_df.describe())

## Check deduplicated data

pokemon_df.drop_duplicates(inplace=True)

## Check missing data

print(pokemon_df.isnull().sum())
print(combats_df.isnull().sum())
print(test_df.isnull().sum())

### Let's check out the row where a Pokemon name is missing

print(pokemon_df[pokemon_df['Name'].isnull()])
print("This pokemon is before the missing Pokemon: " + pokemon_df['Name'][61])
print("This pokemon is after the missing Pokemon: " + pokemon_df['Name'][63])

# Replace missing values if necessary

pokemon_df['Name'][62] = "Primeape"
pokemon_df['Type_2'] = pokemon_df['Type_2'].fillna('None')

# Export of the cleaned dataset

pokemon_df.to_csv(os.path.join(basedir, 'data/intermediate/pokemon.csv'), index=False)
