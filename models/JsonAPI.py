#! /usr/bin/env python3
# coding: utf-8

"""
This module loads datas form Json API if not already done
"""


import requests
import json
import os

from models.config import *


class Json:

    def __init__(self):
        self.first = None
        self.get_categories()

    def check_first(self):

        path = os.getcwd()
        if os.path.isdir(path + "/data"):
            return False
        else :
            os.mkdir(path + "/data")
            return True

    def get_categories(self):

        if self.check_first() == True:
            print("Récupération des catégories")

            url = 'https://fr.openfoodfacts.org/categories.json'
            data = requests.get(url).json()
            with open('data/categories.json', 'w') as f:
                f.write(json.dumps(data, indent=4))

            self.first = True

        else :
            print("Données actuellement dans la base")

    def get_products(self, categories_info):

        if self.first == True:

            print("Récupération des products")

            for name, urlnames in categories_info.items():
                for i in range (1, (NB_PAGES+1)):
                    url = 'https://world.openfoodfacts.org/cgi/search.pl?search_tag=categories&search_terms='+ urlnames +'&purchase_places=France&page_size='+\
                            str(PRODUCTS_PER_PAGE) +'&page='+ str(i) +'&json=1'
                    data = requests.get(url).json()
                    file = 'data/Products_' + name + str(i) + '.json'
                    with open(file, 'w') as f:
                        f.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    load = Json()
