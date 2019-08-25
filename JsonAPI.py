import requests
import json
import os

from models.config import *

def check_data():
    path = os.getcwd()
    if os.path.isdir(path + "/data"):
        return True
    else :
        os.mkdir(path + "/data")
        return False

def get_datas():
    if check_data() == False :

        print("Récupération des données")
        # load categories
        url = 'https://fr.openfoodfacts.org/categories.json'
        data = requests.get(url).json()
        with open('data/categories.json', 'w') as f:
            f.write(json.dumps(data, indent=4))

        # load products
        for name, urlname in CATEGORIES.items():
            for i in range (1,6):
                url = 'https://world.openfoodfacts.org/cgi/search.pl?search_tag=categories&search_terms='\
                        + urlname + '&purchase_places=France&page=' + str(i) +'&json=1'
                data = requests.get(url).json()
                file = 'data/Products_' + name + str(i) + '.json'
                with open(file, 'w') as f:
                    f.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    get_datas()
