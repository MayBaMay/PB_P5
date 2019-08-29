#! /usr/bin/env python3
# coding: utf-8

"""
This module manage how to read database.
"""

from models.print import Print


class DbRead:
    """
    Get and search data in MySQL database.
    """

    def __init__(self, dbauth):
        self.connect = dbauth
        self.use_app = True
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
        return self.use_app


    def main_menu(self):
        """Process main menu of Pur Beurre application"""
        rep = Print.menu()

        if rep == '1':  #user chose to find a substitute of a product
            self.get_categories_list()

        elif rep == '2':
            self.get_watchlist()  #user chose to see saved substitutes

        elif rep == '3':  #user choose to quit
            if Print.exit() is True:  # if user confirmed
                self.use_app = False
            else:
                self.main_menu()  # start again

    def get_categories_list(self):
        """Get category list from database"""
        query = ("SELECT categories.num, categories.name \
            FROM categories")
        cursor = self.get_data(query)
        data = cursor.fetchall()
        self.categories_list = data

        Print.result(self.categories_list, 'list_categories')  # print list of categories
        self.categories_menu()  # call method to process the category's choice

    def categories_menu(self):
        """This method process user's choice when suppose to choose a category"""
        while True:
            self.cat_choice = Print.category_choice()

            try:
                repint = int(self.cat_choice)
                if repint == 0:  # if user choose main menu
                    self.main_menu()
                    break
                elif repint == -1:  #if user choose category list
                    self.get_categories_list()
                    break

                else:  # if user enter a category number
                    self.get_products_list()
                    break

            except ValueError:  # if user choose 'F' keyword research
                self.keyword_research_menu(Print.keyword_research(), 'categories')

    def get_products_list(self):
        """This method get procuct's datas to display from database"""
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
        cursor = self.get_data(query, (self.cat_choice,))
        data = cursor.fetchall()
        Print.result(data, 'produis_list')
        self.products_menu()

    def products_menu(self):
        """This method process user's choice when suppose to choose a product"""
        while True:
            self.prod_choice = Print.product_choice()

            try:
                repint = self.prod_choice

                if repint == 0:  # if user choose main menu
                    self.main_menu()
                    break

                elif repint == -1:
                    self.get_categories_list()
                    break

                else:
                    self.valid_product()
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
                    if data != []:
                        print("Vous avez choisi le produit suivant : ")
                        Print.result(data, 'produis_list')
                        self.get_substitute_list()
                        self.main_menu()
                        break

            except ValueError: # user choose 'F' keyword research
                self.keyword_research_menu(Print.keyword_research(), 'products')


    def valid_product(self):
        """This method checks if chosen products is in chosen category"""
        # create list of product's numbers of chosen category
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
        for num in data:
            num_list.append(num[0])

        # check if input in the list
        if repint not in num_list:
            if Print.prod_not_in_category() == '1':
                self.get_categories_list()

    def keyword_research_menu(self, keyword, data_type):
        """Process user choice while asks for a keyword research"""

        if keyword == '0':
            self.main_menu()

        elif keyword == '-1':
            self.get_categories_list()

        else:

            if data_type == 'categories':
                query = ("SELECT * FROM Categories WHERE name like %s")
                cursor = self.get_data(query, ('%'+ keyword +'%',))
                data = cursor.fetchall()
                if data != []:
                    Print.result(data, 'categories_details')
                else:
                    print("Aucune catégorie contenant ce mot clé")

            elif data_type == 'products':
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
                cursor = self.get_data(query, (self.cat_choice, '%'+keyword +'%',))
                data = cursor.fetchall()
                if data != []:
                    Print.result(data, 'produis_list')
                else:
                    print("Aucun produit contenant ce mot clé")


    def get_substitute_list(self):
        """ This method get a substitute whith a better nutriscore from the same category"""
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

        if data == []:
            print("Aucun substitut trouvé dans cette catégorie")
        else:
            Print.result(data, 'show_substitute')
            self.substitute_menu(cursor, num_substitut)

    def substitute_menu(self, cursor, num_substitut):
        """Process user choice to save substitute"""
        if Print.save_substitute():
            update_query = ("UPDATE Produits SET favoris = CURRENT_DATE WHERE num =  %s")
            cursor.execute(update_query, (num_substitut,))
            self.connect.commit()

    def get_watchlist(self):
        """This method display the watchlist of substitutes"""
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
        if data == []:
            print(" Vous n'avez encore enregistré aucun substitut")
        else:
            Print.result(data, 'saved_substitute')
            self.main_menu()
