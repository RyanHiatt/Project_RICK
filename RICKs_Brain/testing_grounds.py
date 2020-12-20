import json
import requests
import csv
import pandas as pd

# r = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=11007')
# print(r)
# decoded_json = json.loads(r.text)
# print(decoded_json)
# print(json.dumps(decoded_json, indent=2))


# with open('../Dataframe/DrinkDB.json', 'r') as file:
#     drink_db = json.load(file)
#
# print(drink_db['drinks'][0]['ingredients']['ingredient0'])

# for i in drinkdb['drinks'][0]['id']:
#     print(i)


on_hand = pd.read_csv('../Dataframe/OnHand.csv')
print(on_hand.loc[2, 'Name'])


# drinkdb = pd.read_json('../Dataframe/DrinkDB.json')
#
# print(drinkdb)