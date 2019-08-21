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
            insert_query = "INSERT INTO categories (id, name, url, products) \
            VALUES (%(id)s, %(name)s, %(url)s, %(products)s)"
            cursor.execute(insert_query, category)
            self.connect.commit()
