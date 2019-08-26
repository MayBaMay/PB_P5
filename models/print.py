#! /usr/bin/env python3
# coding: utf-8

from models.config import *


class Print:


    @staticmethod
    def accueil():
        rep = 0
        loop = True
        while loop :
            print("\n")
            print("1 - Quel aliment souhaitez vous remplacer ?")
            print("2 - Retrouver mes aliments substitués")
            print("3 - Quitter le programme")
            print("\n")
            try :
                rep = int(input("Votre Choix (1, 2 ou 3): "))
                if rep not in [1, 2, 3] :
                    print("Valeur incorrecte.")
                else :
                    return rep
                    break
            except ValueError :
                print("Valeur incorrecte.")

    @staticmethod
    def category_choice():

        rep = 0
        loop = True
        while loop :
            print("CHOIX DE LA CATÉGORIE")
            rep = input("Veuillez choisir une catégorie et entrer ici le chiffre correspondant \n \
                (ou tapez une partie du nom pour afficher la requête) : ")
            print("\n")
            try :
                repint = int(rep)
                if repint not in range(1, NB_CATEGORIES) :
                    print("Valeur incorrecte")
                else :
                    return rep
                    break
            except ValueError :
                return rep

    @staticmethod
    def product_choice():
        rep = 0
        loop = True
        while loop :
            print("CHOIX DU PRODUIT")
            rep = input("Veuillez choisir un produit et entrer ici le chiffre correspondant \n \
                (ou tapez une partie du nom pour afficher la requête) : ")
            print("\n")
            return rep



    @staticmethod
    def result(data, type, rep=0):
        """
        Print data contained in Mysql request
        """
        if type == 'list_categories' :

            if rep == 1 :
                print(" \n")
                print("Liste des catégories : ")
                print(" \n")

                print("{:^4}   {:100}".format('n°', 'nom'))
                print("{:^4}   {:100}".format('-'*4, '-'*100))
                for row in data:
                    print("{:^4} : {:100}".format(row[0], row[1]))
                print(" \n")

        if type == 'categories_details' :
            print("{:^4}   {:50}   {:100}".format('n°', 'nom', 'url'))
            print("{:^4}   {:50}   {:100}".format('-'*4, '-'*50, '-'*100))
            for row in data :
                print("{:^4} : {:50} : {:100}".format(row[0],row[2], row[3]))
            print(" \n")

        if type == 'produis_list' :
            print("{:^4}   {:50}   {:50}   {:^10}".format('n°', 'nom', 'catégorie', 'nutriscore'))
            print("{:^4}   {:50}   {:50}   {:^10}".format('-'*4, '-'*50, '-'*50, '-'*10))
            for row in data :
                print("{:^4}   {:50}   {:50}   {:^10}".format(row[0],row[1], row[2], row[3]))
            print(" \n")

        if type =='show_substitute' :
            pass
