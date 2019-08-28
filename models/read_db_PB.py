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
        self.on = True
        self.nutriscore = ""
        self.cat_choice = ""
        self.prod_choice = ""
        self.categories_list = []

    def get_data(self, query, value=None):
        """
        Get data from database using methods from class instance DbAuth
        """
        cursor = self.connect.create_cursor()
        cursor.execute("USE dbPurBeurre")
        cursor = self.connect.create_cursor()
        cursor.execute(query, value)
        return cursor

    def exit(self):
        """
        This method returns to the application if user wants to quit or continu
        """
        return self.on


    def get_started(self):
        """
        This method is the main menu of the application
        """

        rep = Print.menu()

        if rep == '1' :  #user chose to find a substitute of a product
            query = ("SELECT categories.num, categories.name \
                FROM categories"
                )
            cursor = self.get_data(query)
            data = cursor.fetchall()
            self.categories_list = data

            Print.result(self.categories_list, 'list_categories')  # print list of categories
            self.get_cat_choice()  # call method to process the category's choice

        elif rep == '2' :
            self.get_favoris()  #user chose to see saved substitutes

        elif rep == '3' :  #user chose to quit
            if Print.exit() == True :  # if user confirmed
                self.on = False
            else :
                self.get_started()  # start again


    def get_cat_choice(self):
        loop = True
        while loop :
            self.cat_choice = Print.category_choice()
            if self.cat_choice.isnumeric() :

                if self.cat_choice == '0' :
                    if Print.exit() == True :
                        self.on = False
                        break
                else :
                    query = ("SELECT * FROM Categories WHERE num = %s")
                    cursor = self.get_data(query, (self.cat_choice ,))
                    data = cursor.fetchall()
                    self.get_products()
                    break

            else :
                if self.cat_choice =='-1' :
                    self.get_started()
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
                query = ("SELECT Produits.num \
                        FROM Produits \
                        INNER JOIN Asso_Prod_Cat ON Produits.id = Asso_Prod_Cat.id_produits\
                        INNER JOIN Categories ON Categories.num = Asso_Prod_Cat.num_categories\
                        WHERE Categories.num =  %s\
                        ")
                cursor = self.get_data(query, (self.cat_choice,))
                data = cursor.fetchall()
                num_list = []
                for num in data :
                    num_list.append(num[0])

                if repint not in num_list and repint != 0 :
                    if Print.back_to_categories() == '1':
                        Print.result(self.categories_list, 'list_categories')
                        self.get_cat_choice()
                else :
                    if self.prod_choice == '0' :
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

                if self.prod_choice == '-1' :
                    self.get_started()

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
        if data == [] :
            print(" Vous n'avez encore enregistré aucun substitut")
        else :
            Print.result(data, 'saved_substitute')
            self.get_started()



if __name__ == '__main__':
    pass
