#! /usr/bin/env python3
# coding: utf-8

from models.config import *


class Print:


    @staticmethod
    def menu():
        rep = 0
        loop = True
        while loop :
            print("\n")
            print("MENU PRINCIPAL")
            print("1 - Quel aliment souhaitez vous remplacer ?")
            print("2 - Retrouver mes aliments substitués")
            print("3 - Quitter le programme")
            print("\n")
            rep = input("Votre Choix (1, 2 ou 3): ")
            try :
                repint = int(rep)
                if repint not in [1, 2, 3] :
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
                (ou tapez une partie du nom pour afficher la requête)\n \
                (ou '-1' pour revenir au menu principal)\n \
                (ou '0' pour quitter le programme):\n ")
            print("\n")
            try :
                repint = int(rep)
                if repint not in range(1, NB_CATEGORIES+1) and repint not in [0,-1]:
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
            rep = input("Veuillez choisir un produit dans la liste et entrer ici le chiffre correspondant \n \
                (ou tapez une partie du nom pour afficher la requête)\n \
                (ou '-1' pour revenir au menu principal)\n \
                (ou '0' pour quitter le programme): \n")
            print("\n")
            return rep

    @staticmethod
    def back_to_categories() :
        rep = 0
        rep = input("Le produit sélectionné ne fait pas partie de la catégorie choisie\n \
                Pour sélectionner une autre catégorie tapez '1' sinon tapez entrée : ")
        print("\n")
        return rep


    @staticmethod
    def exit() :
        while True :
            rep = input("Êtes vous sûr de vouloir quitter ? (1=oui, 2=non) : ")
            try :
                repint = int(rep)
                if repint not in [1,2]:
                    print("Valeur incorrecte")
                else :
                    if repint == 1 :
                        return True
                        break
                    elif repint == 2 :
                        return False
                        break
            except ValueError :
                print("Valeur incorrecte")



    @staticmethod
    def save_substitute() :
        while True:
            rep = input("Voulez-vous enregistrer ce substitut ? (1=oui, 2=non) : ")
            try :
                repint = int(rep)
                if repint not in [1,2]:
                    print("Valeur incorrecte")
                else :
                    if repint == 1 :
                        return True
                        break
                    elif repint == 2 :
                        return False
                        break
            except ValueError :
                print("Valeur incorrecte")

    @staticmethod
    def result(data, type):
        """
        Print data contained in Mysql request
        """
        if type == 'list_categories' :
            print(" \n")
            print("Liste des catégories : ")
            print(" \n")
            print("{:^4}   {:100}".format('N°', 'Nom'))
            print("{:^4}   {:100}".format('-'*4, '-'*100))
            for row in data:
                print("{:^4} : {:100}".format(row[0], row[1]))
            print(" \n")

        if type == 'categories_details' :
            print("{:^4}   {:50}   {:100}".format('N°', 'Nom', 'Url'))
            print("{:^4}   {:50}   {:100}".format('-'*4, '-'*50, '-'*100))
            for row in data :
                print("{:^4} : {:50} : {:100}".format(row[0],row[2], row[3]))
            print(" \n")

        if type == 'produis_list' :
            print("{:^4}   {:50}   {:50}   {:^10}".format('N°', 'Nom', 'Catégorie', 'Nutriscore'))
            print("{:^4}   {:50}   {:50}   {:^10}".format('-'*4, '-'*50, '-'*50, '-'*10))
            for row in data :
                print("{:^4}   {:50}   {:50}   {:^10}".format(row[0],row[1], row[2], row[3]))
            print(" \n")

        if type =='show_substitute' :
            print("Substitut trouvé : ")
            for row in data :
                print("N° : {}\nNom : {}\nNutriscore : {}\nMarques : {}\nPoints de vente : {}\nUrl : {}"
                .format(row[0],row[1], row[2], row[3], row[4], row[5]))
            print(" \n")

        if type == 'saved_substitute' :
            print("Substituts enregistrés :")
            print(" \n")
            for row in data :
                print("date : {} | N° : {} | Nom : {} | Nutriscore : {} | Marques : {} | Points de vente :{} | url :{} | Catégorie :{}"
                    .format(row[0],row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                print(" \n")
