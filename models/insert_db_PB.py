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
            self.truncate_datas("categories", category)

            cursor = self.connect.create_cursor()
            insert_query = "INSERT INTO Categories (id, name, url, products) \
            VALUES (%(id)s, %(name)s, %(url)s, %(products)s)"
            cursor.execute(insert_query, category)
            self.connect.commit()

    def insert_products(self):

        products_infos_list = []
        categories_names_list = []
        categories_num_list = []

        print("loading products in databes...")
        for name in CATEGORIES.keys() :
            for i in range (1,6):
                file = 'data/Products_' + name + str(i) +'.json'
                with open(file, "r", encoding="utf8") as data:
                    data_json = json.load(data)
                    for prod in data_json["products"] :
                        try :
                            products_infos_list.append({"id" : prod["id"],
                                    "product_name" : prod["product_name"],
                                    "nutrition_grade_fr" : prod["nutrition_grade_fr"],
                                    "brands" : prod["brands"],
                                    "stores" : prod["stores"],
                                    "url" : prod["url"]
                                    })
                            categories_names_list.append(prod["categories_hierarchy"])
                        except KeyError :
                            pass

        print("truncate datas & insert products in database ")

        # insert datas in table Produits
        for prod in products_infos_list:
            self.truncate_datas("products", prod)

            cursor = self.connect.create_cursor()
            insert_query = "INSERT INTO Produits (id, product_name, nutrition_grade_fr, brands, stores, url) \
            VALUES (%(id)s, %(product_name)s, %(nutrition_grade_fr)s, %(brands)s, %(stores)s, %(url)s) \
            ON DUPLICATE KEY UPDATE id = id"
            cursor.execute(insert_query, prod)
            self.connect.commit()

        # recovery category num from ids in Json categories_hierarchy
        for cat_id_list in categories_names_list:
            n = []
            for cat_id in cat_id_list:
                cursor = self.connect.create_cursor()
                name_cat_query = "SELECT num FROM Categories WHERE id = %s"
                cursor.execute(name_cat_query, (cat_id,))
                data = cursor.fetchone()
                if data != None :
                    n.append(data[0])
            categories_num_list.append(n)

        # insert datas in table Asso_Prod_Cat
        asso = []
        i = 0

        while i < len(products_infos_list)-1 :
            id =  products_infos_list[i]['id']
            for nb in categories_num_list[i] :
                nb = str(nb)
                info_cat = (nb, id)

                if info_cat not in asso :
                    asso.append(info_cat)
                else :
                    pass
            i += 1

        print('insertion dans Asso_Prod_Cat...')
        cursor = self.connect.create_cursor()
        insert_CatProd_query = "INSERT INTO Asso_Prod_Cat (num_categories, id_produits) \
        VALUES (%s, %s)"
        cursor.executemany(insert_CatProd_query, asso)
        self.connect.commit()


    def truncate_datas(self, type, datas):
        if type == "categories":
            datas["id"] = datas["id"][:80]
            datas["name"] = datas["name"][:80]
            datas["url"] = datas["url"][:255]
            if "sameAs" in datas.keys():
                del datas["sameAs"]
        elif type == "products" :
            datas["id"] = datas["id"][:80]
            datas["product_name"] = datas["product_name"][:80]
            datas["brands"] = datas['brands'][:80]
            datas["stores"] = datas['stores'][:80]
            datas["url"] = datas['url'][:255]
