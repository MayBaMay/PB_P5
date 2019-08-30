#! /usr/bin/env python3
# coding: utf-8

""" Find a product's substitute with  Open Food Facts database"""

from models.print import Print
from models.auth_db import DbAuth
from models.json_api import JsonAPI
from models.sort_datas import SortedDatas
from models.create_db import DbCreate
from models.insert_db import DbInsert
from models.read_db import DbRead


def game_on():
    """Main code for application Pur Beurre"""

    # generate database connexion
    dbauth = DbAuth()
    dbauth.connect()

    # create a JsonAPI instance to start loading datafile
    jload = JsonAPI()

    if jload.first is True:  # if json files not in the repertory

        # Create instances needed for loading datas in database
        sort = SortedDatas(dbauth)
        dbstruc = DbCreate(dbauth)
        insert = DbInsert(dbauth)

        # process categories datas
        jload.get_categories()  # load json file from API
        sort.filtered_categories()  # sort datas before insert in database

        # process products datas
        jload.get_products(sort.categories_info) # load json file from API
        sort.filtered_products()  # sort datas before insert in database

        dbstruc.drop()  # reinitiate database if exits
        dbstruc.create_tables()  # create tables in database

        insert.insert_categories(sort.final_cat)
        insert.insert_products(sort.products_infos_list)

        # get datas for table Asso_prod_cat wich links products and categories
        sort.get_categories_per_product()
        insert.insert_prod_cat(sort.asso)

    # Generate an instance of the class DbRead to read datas in database
    read = DbRead(dbauth)

    while read.exit() is True:

        read.main_menu()

if __name__ == "__main__":

    Print.licence_off()
    game_on()
