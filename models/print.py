#! /usr/bin/env python3
# coding: utf-8


class Print:

    def __init__(self):
        self.input = input



    def accueil(self):
        loop = True
        while loop :
            print("\n")
            print("1 - Quel aliment souhaitez vous remplacer ?")
            print("2 - Retrouver mes aliments substitués")
            print("3 - Quitter le programme")
            print("\n")
            try :
                self.input = int(input("Votre Choix (1, 2 ou 3): "))
                break
            except ValueError :
                print("Valeur incorrecte.")
        return self.input


    def choix_categorie (self):
        if self.input == 1 :
            print("Liste des catégories : ")



if __name__ == "__main__" :
    rep = Print()
    rep_accueil = rep.accueil()
    print(type(rep_accueil))
