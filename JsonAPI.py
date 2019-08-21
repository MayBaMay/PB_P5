import requests
import json

import * from config

def get_categories():
    for category in CATEGORIES :
        url = 'https://fr.openfoodfacts.org/categories' + category + '.json'
        data = requests.get(url).json()
        with open('data/categories.json', 'w') as f:
            f.write(json.dumps(data, indent=4))

def get_products(categorie):
    url = 'https://world.openfoodfacts.org/cgi/search.pl?search_tag=categories&search_terms='\
            + categorie + '&page_size=1&json=1'
    data = requests.get(url).json()
    file = 'data/Products_' + categorie + '.json'
    with open(file, 'w') as f:
        f.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    get_products('chocolat')
