#! /usr/bin/env python3
# coding: utf-8

"""
This module sorts datas loaded from OpenFoodFects API
"""

import mysql.connector
import json
import requests
from models.config import *


class Sorted_datas:
    """
    This class allowed to filter, truncate, link and get datas
    from the API loaded datas
    """

    def __init__(self, dbauth):
        self.connect = dbauth  # database connection with class Dbauth instance

        self.list_filtered_cat = []
        self.final_cat = []

        self.categories_info = {}

        self.products_infos_list = []
        self.categories_names_list = []
        self.categories_num_list = []
        self.asso = []



    def filtered_categories(self):
        """ Get categories datas in a list so they can be treated as needed"""

        with open("data/categories.json", "r", encoding="utf8") as data:
            data_json = json.load(data)
            final_cat = []
            for item in data_json["tags"] :
                self.list_filtered_cat.append(item)

        i = 0
        for cat in self.list_filtered_cat :
            # limit the number of categories to the number chosen in config
            if i < NB_CATEGORIES :
                # limit the categories to the ones which have a lot of products
                if cat["products"] > 10000:
                    self.final_cat.append(cat)
                    i += 1

        self.truncate_datas("categories")
        self.get_info_from_categories()

    def get_info_from_categories(self):
        """
        This method get datas needed to load products pages with Json class
        """

        cat_url_names = []
        cat_names = []

        for category in self.final_cat :
            # get only names of categories in the url to use it for API search requests
            url = category["url"]
            url = url[39:]
            cat_url_names.append(url)
            # get names of categories to name related files
            cat_names.append(category["name"])
            # create a dictionnary for each category with those elements
            self.categories_info = {x:y for x,y in zip(cat_names, cat_url_names)}


    def filtered_products(self):

        for name in self.categories_info.keys() :
            for i in range (1,(NB_PAGES + 1)):
                file = 'data/Products_' + name + str(i) +'.json'
                with open(file, "r", encoding="utf8") as data:
                    data_json = json.load(data)
                    for prod in data_json["products"] :
                        try :
                            self.products_infos_list.append({"id" : prod["id"],
                                    "product_name" : prod["product_name"],
                                    "nutrition_grade_fr" : prod["nutrition_grade_fr"],
                                    "brands" : prod["brands"],
                                    "stores" : prod["stores"],
                                    "url" : prod["url"]
                                    })
                            self.categories_names_list.append(prod["categories_hierarchy"])
                        except KeyError :
                            pass

        self.truncate_datas("products")

    def truncate_datas(self, type):
        """ truncate datas to sizes defined for each element in the database"""

        if type == "categories":
            for cat in self.final_cat :
                cat["id"] = cat["id"][:80]
                cat["name"] = cat["name"][:80]
                cat["url"] = cat["url"][:255]
                if "sameAs" in cat.keys():
                    del cat["sameAs"]

        elif type == "products" :
            for prod in self.products_infos_list :
                prod["id"] = prod["id"][:80]
                prod["product_name"] = prod["product_name"][:80]
                prod["brands"] = prod['brands'][:80]
                prod["stores"] = prod['stores'][:80]
                prod["url"] = prod['url'][:255]


    def get_categories_per_product(self):
        """
        This method get datas to insert in the table Asso_Prod_Cat
        wich links products and categories
        NB : a product can belong to more than one category
        """

        # recover categories number for each products from ids in Json categories_hierarchy
        for categories in self.categories_names_list:
            n = []
            for cat_id in categories:
                cursor = self.connect.create_cursor()
                name_cat_query = "SELECT num FROM Categories WHERE id = %s"
                cursor.execute(name_cat_query, (cat_id,))
                data = cursor.fetchone()
                if data != None :
                    n.append(data[0])
            self.categories_num_list.append(n)

        # Create a dictionnary with product's id and related category's number
        i = 0
        while i < len(self.products_infos_list)-1 :
            id =  self.products_infos_list[i]['id']   #get product's id

            for nb in self.categories_num_list[i] :  # get num category
                nb = str(nb)

                info_cat = (nb, id)

                if info_cat not in self.asso :  # check if not duplication
                    self.asso.append(info_cat)
                else :
                    pass
            i += 1
