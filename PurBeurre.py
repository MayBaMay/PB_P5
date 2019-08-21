#! /usr/bin/env python3
# coding: utf-8

import os
import sys

import JsonAPI
import models.auth_db_PB as auth_db_PB
from models import create_db_PB
from models import insert_db_PB
from models.config import *



JsonAPI.get_categories()

dbauth = auth_db_PB.DbAuth()
dbauth.connect()

dbstruc = create_db_PB.DbCreate(dbauth)
dbstruc.drop()
dbstruc.create_database()
dbstruc.create_tables()

insert_sql = insert_db_PB.DbInsert(dbauth)
insert_sql.insert_categories()
