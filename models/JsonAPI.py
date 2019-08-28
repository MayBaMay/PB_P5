#! /usr/bin/env python3
# coding: utf-8

"""
This module loads datas from Json API if not already done
"""

import requests
import json
import os

from models.config import *


class JsonAPI:

    def __init__(self):
        self.first = None
        self.check_first()

    def check_first(self):
        """
        This method checks if data repertory exists or not
        If it does exists, it means the datas had been already loaded
        """
        path = os.getcwd()
        if os.path.isdir(path + "/data"):
            self.first = False
            print("Données actuellement dans la base")
        else :
            os.mkdir(path + "/data")
            self.first = True
            print("Chargement de la base de donnée, veuillez patienter ...")

    def get_categories(self):
        """
        This method loads categories from OpenFoodFacts API
        and create a json file with datas
        """

        url = 'https://fr.openfoodfacts.org/categories.json'
        data = requests.get(url).json()
        with open('data/categories.json', 'w') as f:
            f.write(json.dumps(data, indent=4))


    def get_products(self, categories_info):
        """
        This method loads products from OpenFoodFacts API
        This method is called after sorting datas with Sorted_datas class
        which defines which categories to get and allow to get informations
        such as names (for file's names) and url names (to call urls)
        """

        for name, urlnames in categories_info.items():
            for i in range (1, (NB_PAGES+1)):
                url = 'https://world.openfoodfacts.org/cgi/search.pl?search_tag=categories&search_terms='+ urlnames +'&purchase_places=France&page_size='+\
                        str(PRODUCTS_PER_PAGE) +'&page='+ str(i) +'&json=1'
                data = requests.get(url).json()
                file = 'data/Products_' + name + str(i) + '.json'
                with open(file, 'w') as f:
                    f.write(json.dumps(data, indent=4))
