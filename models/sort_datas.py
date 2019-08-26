#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
import json
import requests
from models.config import *


class Sorted_datas:

    def __init__(self, dbauth):
        self.connect = dbauth
        self.list_filtered_cat = []
        self.final_cat = []

        self.categories_info = {}

        self.products_infos_list = []
        self.categories_names_list = []
        self.categories_num_list = []
        self.asso = []

        self.filtered_categories()
        self.get_info_from_categories()


    def filtered_categories(self):

        print("tri des catégories avant insertion dans base de donnée..")

        with open("data/categories.json", "r", encoding="utf8") as data:
            data_json = json.load(data)
            final_cat = []
            for item in data_json["tags"] :
                self.list_filtered_cat.append(item)

        i = 0
        for cat in self.list_filtered_cat :
            if i < NB_CATEGORIES :
                if cat["products"] > 10000:
                    self.final_cat.append(cat)
                    i += 1

        self.truncate_datas("categories")

    def get_info_from_categories(self):

        cat_url_names = []
        cat_names = []

        for category in self.final_cat :
            url = category["url"]
            url = url[39:]
            cat_url_names.append(url)
            cat_names.append(category["name"])
            self.categories_info = {x:y for x,y in zip(cat_names, cat_url_names)}


    def filtered_products(self):

        print("tri des produits avant insertion dans base de donnée...")
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


    def get_cat_per_prod(self):
        # recovery category num from ids in Json categories_hierarchy
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

        i = 0
        while i < len(self.products_infos_list)-1 :
            id =  self.products_infos_list[i]['id']
            for nb in self.categories_num_list[i] :
                nb = str(nb)
                info_cat = (nb, id)

                if info_cat not in self.asso :
                    self.asso.append(info_cat)
                else :
                    pass
            i += 1
