#! /usr/bin/env python3
# coding: utf-8

"""
This module manage insertion database.
"""


class DbInsert:
    """
    Insert data in MySQL database.
    """

    def __init__(self, dbauth):
        self.connect = dbauth

    def insert_categories(self, categrories):
        """
        Insert categories in table Categories
        """

        for category in categrories:
            cursor = self.connect.create_cursor()
            insert_query = "INSERT INTO Categories (id, name, url, products) \
            VALUES (%(id)s, %(name)s, %(url)s, %(products)s)"
            cursor.execute(insert_query, category)
            self.connect.commit()


    def insert_products(self, products):
        """
        insert products in table Produits
        """

        for prod in products:
            cursor = self.connect.create_cursor()
            insert_query = "INSERT INTO Produits \
            (id, product_name, nutrition_grade_fr, brands, stores, url) \
            VALUES (%(id)s, %(product_name)s, %(nutrition_grade_fr)s, %(brands)s, %(stores)s, %(url)s) \
            ON DUPLICATE KEY UPDATE id = id"
            cursor.execute(insert_query, prod)
            self.connect.commit()


    def insert_prod_cat(self, data):
        """
        Insert links between products and category in table Asso_Prod_Cat
        """

        cursor = self.connect.create_cursor()
        insert_query = "INSERT INTO Asso_Prod_Cat (id_categories, id_produits) \
        VALUES (%s, %s)"
        cursor.executemany(insert_query, data)
        self.connect.commit()
