#! /usr/bin/env python3
# coding: utf-8

"""
This module loads datas from Json API if not already done
"""


import os
import json
import requests

from models.config import NB_PAGES, PRODUCTS_PER_PAGE

class JsonAPI:
    """This class generates loading datas from API"""

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
        else:
            os.mkdir(path + "/data")
            self.first = True
            print("Chargement de la base de donnée, veuillez patienter ...")

    @staticmethod
    def get_categories():
        """
        This method loads categories from OpenFoodFacts API
        and create a json file with datas
        """

        url = 'https://fr.openfoodfacts.org/categories.json'
        data = requests.get(url).json()
        with open('data/categories.json', 'w') as file:
            file.write(json.dumps(data, indent=4))

    @staticmethod
    def get_products(categories_info):
        """
        This method loads products from OpenFoodFacts API
        This method is called after sorting datas with Sorted_datas class
        which defines which categories to get and allow to get informations
        such as names (for file's names) and url names (to call urls)
        """

        for name, urlnames in categories_info.items():
            for i in range(1, (NB_PAGES+1)):
                url = 'https://world.openfoodfacts.org/cgi/search.pl?\
                    search_tag=categories&search_terms={}&\
                    purchase_places=France&page_size={}&page={}&json=1'.format(
                        urlnames, str(PRODUCTS_PER_PAGE), str(i))
                data = requests.get(url).json()
                name_file = 'data/Products_' + name + str(i) + '.json'
                with open(name_file, 'w') as file:
                    file.write(json.dumps(data, indent=4))
