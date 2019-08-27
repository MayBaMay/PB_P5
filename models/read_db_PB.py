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
        self.cat_choice = ""
        self.prod_choice = ""
        self.on = False


    def get_data(self, query, value=None):
        """
        Get data from database.
        """
        cursor = self.connect.create_cursor()
        cursor.execute("USE dbPurBeurre")
        cursor = self.connect.create_cursor()
        cursor.execute(query, value)
        return cursor

    def exit(self):
        return self.on


    def get_started(self):
        query = ("SELECT categories.num, categories.name \
            FROM categories"
            )
        cursor = self.get_data(query)
        data = cursor.fetchall()
        rep = Print.accueil()

        if rep == '1' :
            Print.result(data, 'list_categories', rep)
            self.get_cat_choice()

        elif rep == '2' :
            self.get_favoris()

        elif rep == '3' :
            if Print.exit() == True :
                self.on = False
            else :
                self.get_started()


    def get_cat_choice(self):
        loop = True
        while loop :
            self.cat_choice = Print.category_choice()
            if self.cat_choice.isnumeric() :
                query = ("SELECT * FROM Categories WHERE num = %s")
                cursor = self.get_data(query, (self.cat_choice ,))
                data = cursor.fetchall()
                self.get_products()
                break

            elif self.cat_choice == '§' :
                self.get_started()
                break

            elif self.cat_choice == 'q' or self.cat_choice == 'Q' :
                if Print.exit() == True :
                    self.on = False
                    break

            else :
                query = ("SELECT * FROM Categories WHERE name like %s")
                cursor = self.get_data(query, ('%'+ self.cat_choice +'%',))
                data = cursor.fetchall()
                if data != [] :
                    Print.result(data, 'categories_details')

    def get_products(self):
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
        cursor = self.get_data(query, (self.cat_choice ,))
        data = cursor.fetchall()
        Print.result(data, 'produis_list')
        self.get_prod_choice()

    def get_prod_choice(self) :
        loop = True
        while loop :
            self.prod_choice = Print.product_choice()
            if self.prod_choice.isnumeric() :
                # check if input is in product's numbers
                repint = int(self.prod_choice)
                query = ("SELECT num FROM Produits")
                cursor = self.get_data(query)
                data = cursor.fetchall()
                num_list = []
                for num in data :
                    num_list.append(num[0])

                if repint not in num_list :
                    print("Valeur incorrecte")
                else :
                    query = ("SELECT Produits.num,\
                                produits.product_name,\
                                GROUP_CONCAT(DISTINCT Categories.name,' ') AS categories,\
                                Produits.nutrition_grade_fr\
                            FROM Produits\
                            INNER JOIN Asso_Prod_Cat ON Produits.id = Asso_Prod_Cat.id_produits\
                            INNER JOIN Categories ON Categories.num = Asso_Prod_Cat.num_categories\
                            WHERE Categories.num =  %s\
                                AND produits.num = %s\
                            GROUP BY Produits.id\
                            ORDER BY Produits.num\
                            ")
                    cursor = self.get_data(query, (self.cat_choice, self.prod_choice,))
                    data = cursor.fetchall()
                    if data != [] :
                        print("Vous avez choisi le produit suivant : ")
                        Print.result(data, 'produis_list')
                    self.get_substitute()
                    break
            else :

                if self.prod_choice == '§' :
                    self.get_started()
                elif self.prod_choice == 'q' or self.prod_choice == 'Q' :
                    if Print.exit() == True :
                        self.on = False
                        break
                    else :
                        self.get_products()
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
                    cursor = self.get_data(query, (self.cat_choice, '%'+self.prod_choice +'%',))
                    data = cursor.fetchall()
                    if data != [] :
                        Print.result(data, 'produis_list')

    def get_substitute (self):
        query = ("SELECT Produits.num,\
                    Produits.product_name,\
                    Produits.nutrition_grade_fr,\
                    Produits.brands,\
                    Produits.stores,\
                    Produits.url,\
                	GROUP_CONCAT(DISTINCT Categories.name,' ') AS categories\
                FROM Produits\
                INNER JOIN Asso_Prod_Cat ON Produits.id = Asso_Prod_Cat.id_produits\
                INNER JOIN Categories ON Categories.num = Asso_Prod_Cat.num_categories\
                WHERE Produits.nutrition_grade_fr <=\
                    (SELECT Produits.nutrition_grade_fr FROM Produits WHERE Produits.num = %s)\
                    AND Categories.num = %s\
                GROUP BY Produits.id\
                ORDER BY Produits.nutrition_grade_fr\
                LIMIT 1\
                ")
        cursor = self.get_data(query, (self.prod_choice, self.cat_choice,))
        data = cursor.fetchall()
        num_substitut = str(data[0][0])

        if data == [] :
            print("Aucun substitut trouvé dans cette catégorie")
        else :
            Print.result(data, 'show_substitute')
            if Print.save_substitute() :
                update_query = ("UPDATE Produits SET favoris = CURRENT_DATE WHERE num =  %s")
                cursor.execute(update_query, (num_substitut,))
                self.connect.commit()

        self.get_started()

    def get_favoris(self):
        query = ("SELECT Produits.favoris,\
                    Produits.num,\
                    Produits.product_name,\
                    Produits.nutrition_grade_fr,\
                    Produits.brands,\
                    Produits.stores,\
                    Produits.url,\
                	GROUP_CONCAT(DISTINCT Categories.name,' ') AS categories\
                FROM Produits\
                INNER JOIN Asso_Prod_Cat ON Produits.id = Asso_Prod_Cat.id_produits\
                INNER JOIN Categories ON Categories.num = Asso_Prod_Cat.num_categories\
                WHERE Produits.favoris IS NOT NULL\
                GROUP BY Produits.id\
                ORDER BY Produits.favoris DESC\
                ")
        cursor = self.get_data(query)
        data = cursor.fetchall()
        Print.result(data, 'saved_substitute')


if __name__ == '__main__':
    pass
