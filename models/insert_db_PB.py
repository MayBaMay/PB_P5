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

        cat = []
        with open("data/categories.json", "r", encoding="utf8") as data:
            data_json = json.load(data)
            for item in data_json["tags"] :
                cat.append(item)

        for category in cat :

            category["id"] = category["id"][:80]
            category["name"] = category["name"][:80]
            category["url"] = category["url"][:255]

            if "sameAs" in category.keys():
                del category["sameAs"]

            cursor = self.connect.create_cursor()
            insert_query = "INSERT INTO Categories (id, name, url, products) \
            VALUES (%(id)s, %(name)s, %(url)s, %(products)s)"
            cursor.execute(insert_query, category)
            self.connect.commit()

    def insert_products(self):

        products =[]
        for name in CATEGORIES.keys() :
            file = 'data/Products_' + name + '.json'
            with open(file, "r", encoding="utf8") as data:
                data_json = json.load(data)
                for prod in data_json["products"] :
                    if not prod["nutrition_grade_fr"] :
                        pass
                    else :
                        products.append({"id" : prod["id"],
                                "product_name" : prod["product_name"],
                                "nutrition_grade_fr" : prod["nutrition_grade_fr"],
                                "brands" : prod["brands"],
                                "stores" : prod["stores"],
                                "url" : prod["url"]
                                })

        for prod in products:
            prod["id"] = prod["id"][:80]
            prod["product_name"] = prod["product_name"][:80]
            prod["brands"] = prod['brands'][:80]
            prod["stores"] = prod['stores'][:80]
            prod["url"] = prod['url'][:255]

            cursor = self.connect.create_cursor()
            insert_query = "INSERT INTO Products (id, product_name, nutrition_grade_fr, stores, url) \
            VALUES (%(id)s, %(product_name)s, %(nutrition_grade_fr)s, %(stores)s, %(url)s)"
            cursor.execute(insert_query, category)
            self.connect.commit()
