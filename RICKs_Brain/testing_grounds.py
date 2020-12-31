import json

with open('../Dataframe/DrinkDB.json', 'r') as file:
    drink_db = json.load(file)

drink_profile = drink_db['drinks'][1]
for key, value in drink_profile['ingredients'].items():
    print(key, value)