#! /usr/bin/env python3
# coding: utf-8

"""
This module manage MySQL database.
"""

import mysql.connector
import json
from models.config import *

class DbInsert:
    """
    Insert data in MySQL database.
    """

    def __init__(self, dbauth):
        self.connect = dbauth

    def insert_categories(self):
        """
        Insert data from json.
        """

        print("loading categories in databes...")
        cat = []
        with open("data/categories.json", "r", encoding="utf8") as data:
            data_json = json.load(data)
            for item in data_json["tags"] :
                cat.append(item)

        print("truncate datas & insert categories in database")
        for category in cat :
            self.truncate_datas('categories', category)

            cursor = self.connect.create_cursor()
            insert_query = "INSERT INTO Categories (id, name, url, products) \
            VALUES (%(id)s, %(name)s, %(url)s, %(products)s)"
            cursor.execute(insert_query, category)
            self.connect.commit()

    def insert_products(self):

        products =[]
        print("loading products in databes...")
        for name in CATEGORIES.keys() :
            for i in range (1,5):
                file = 'data/Products_' + name + str(i) +'.json'
                with open(file, "r", encoding="utf8") as data:
                    data_json = json.load(data)
                    for prod in data_json["products"] :
                        try :
                            products.append({"id" : prod["id"],
                                    "product_name" : prod["product_name"],
                                    "nutrition_grade_fr" : prod["nutrition_grade_fr"],
                                    "brands" : prod["brands"],
                                    "stores" : prod["stores"],
                                    "url" : prod["url"],
                                    "Categorie" : "name"
                                    })
                        except KeyError :
                            pass

        print("truncate datas & insert products in database ")
        for prod in products:
            self.truncate_datas('products', prod)

            cursor = self.connect.create_cursor()
            insert_query = "INSERT INTO Produits (id, product_name, nutrition_grade_fr, stores, url, id_categorie) \
            VALUES (%(id)s, %(product_name)s, %(nutrition_grade_fr)s, %(stores)s, %(url)s, 1)"
            cursor.execute(insert_query, prod)
            self.connect.commit()

    def truncate_datas(self, type, datas):
        if type == 'categories':
            datas["id"] = datas["id"][:80]
            datas["name"] = datas["name"][:80]
            datas["url"] = datas["url"][:255]
            if "sameAs" in datas.keys():
                del datas["sameAs"]
        elif type == 'products' :
            datas["id"] = datas["id"][:80]
            datas["product_name"] = datas["product_name"][:80]
            datas["brands"] = datas['brands'][:80]
            datas["stores"] = datas['stores'][:80]
            datas["url"] = datas['url'][:255]
