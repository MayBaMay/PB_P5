#! /usr/bin/env python3
# coding: utf-8

import os
import sys

import models.auth_db_PB as auth_db_PB
from models.create_db_PB import DbCreate
from models.JsonAPI import Json
from models.insert_db_PB import DbInsert
from models.sort_datas import Sorted_datas
from models.read_db_PB import DbRead
from models.print import Print
from models.config import *



jload = Json()
dbauth = auth_db_PB.DbAuth()
dbauth.connect()

if jload.first == True :
    insert = DbInsert(dbauth)

    dbstruc = DbCreate(dbauth)
    dbstruc.drop()
    dbstruc.create_tables()

    sort = Sorted_datas(dbauth)
    jload.get_products(sort.categories_info)

    insert.insert_categories(sort.final_cat)

    sort.filtered_products()
    insert.insert_products(sort.products_infos_list)

    sort.get_cat_per_prod()
    insert.insert_prod_cat(sort.asso)

read = DbRead(dbauth)

on = True

while on == True :

    read.get_started()
    on = read.exit()
