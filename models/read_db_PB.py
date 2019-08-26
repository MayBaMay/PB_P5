#! /usr/bin/env python3
# coding: utf-8

"""
This module manage how to read database.
"""

import mysql.connector
from models.config import *
from models.print import Print


class DbRead:
    """
    Get and search data in MySQL database.
    """

    def __init__(self, dbauth):
        self.connect = dbauth
        self.nutriscore = ""

    def get_data(self, query, value=None):
        """
        Get data from database.
        """
        cursor = self.connect.create_cursor()
        cursor.execute("USE dbPurBeurre")
        cursor = self.connect.create_cursor()
        cursor.execute(query, value)
        return cursor


    def get_categories(self):
        query = ("SELECT categories.num, categories.name \
            FROM categories"
            )

        cursor = self.get_data(query)
        data = cursor.fetchall()
        Print.result(data, 'list_categories', Print.accueil())
        self.get_cat_choice()


    def get_cat_choice(self):
        loop = True
        while loop :
            rep = Print.category_choice()
            if rep.isnumeric() :
                query = ("SELECT * FROM Categories WHERE num = %s")
                cursor = self.get_data(query, (rep ,))
                data = cursor.fetchall()
                self.get_products(rep)
                break

            else :
                query = ("SELECT * FROM Categories WHERE name like %s")
                cursor = self.get_data(query, ('%'+rep +'%',))
                data = cursor.fetchall()
                if data != [] :
                    Print.result(data, 'categories_details')

    def get_products(self, rep):
        query = ("SELECT Produits.num,\
                    produits.product_name,\
                    GROUP_CONCAT(DISTINCT Categories.name,' ') AS categories,\
                    Produits.nutrition_grade_fr\
                FROM Produits\
                INNER JOIN Asso_Prod_Cat ON Produits.id = Asso_Prod_Cat.id_produits\
                INNER JOIN Categories ON Categories.num = Asso_Prod_Cat.num_categories\
                WHERE Categories.num =  %s\
                GROUP BY Produits.id\
                ORDER BY Produits.num\
                ")
        cursor = self.get_data(query, (rep ,))
        data = cursor.fetchall()
        Print.result(data, 'produis_list')
        self.get_prod_choice(rep)

    def get_prod_choice(self, repCat) :
        loop = True
        while loop :
            rep = Print.product_choice()
            if rep.isnumeric() :
                # check if input is in product's numbers
                repint = int(rep)
                query = ("SELECT num FROM Produits")
                cursor = self.get_data(query)
                data = cursor.fetchall()
                num_list = []
                for num in data :
                    num_list.append(num[0])

                if repint not in num_list :
                    print("Valeur incorrecte")
                else :
                    self.get_substitute(rep)
                    break
            else :
                query = ("SELECT Produits.num,\
                            produits.product_name,\
                            GROUP_CONCAT(DISTINCT Categories.name,' ') AS categories,\
                            Produits.nutrition_grade_fr\
                        FROM Produits\
                        INNER JOIN Asso_Prod_Cat ON Produits.id = Asso_Prod_Cat.id_produits\
                        INNER JOIN Categories ON Categories.num = Asso_Prod_Cat.num_categories\
                        WHERE Categories.num =  %s\
                            AND produits.product_name like %s\
                        GROUP BY Produits.id\
                        ORDER BY Produits.num\
                        ")
                cursor = self.get_data(query, (repCat, '%'+rep +'%',))
                data = cursor.fetchall()
                if data != [] :
                    Print.result(data, 'produis_list')

    def get_substitute (self, rep):
        pass


if __name__ == '__main__':
    pass
