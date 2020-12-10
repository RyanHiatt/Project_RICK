import json
import requests

# r = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=11007')
# print(r)
# decoded_json = json.loads(r.text)
# print(decoded_json)
# print(json.dumps(decoded_json, indent=2))


with open('../Dataframe/DrinkDB.json', 'r') as file:
    drink_db = json.load(file)

print(drink_db['drinks'][0]['img'])

# for i in drinkdb['drinks'][0]['id']:
#     print(i)
