#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
from models.config import *

""" Connecting to MySQL database"""

class DbAuth :
    """Connect to MySQL server"""

    def __init__(self):
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.passwrd = MYSQL_PASSWD
        self.database = MYSQL_DATABASE
        self.PurBeurreConnect = None

    def connect(self):
        try :
            self.PurBeurreConnect = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwrd,
                )
        except mysql.connector.errors.InterfaceError:
            print("Serveur MySQL inaccessible.")
            exit()

    def create_cursor(self):
        return self.PurBeurreConnect.cursor()

    def commit(self):
        return self.PurBeurreConnect.commit()
