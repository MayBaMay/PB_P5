#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
from models.config import *

"""This module manage all operations on MySQL connexion"""

class DbAuth :
    """
    This class allowed to automate all operation on the connexion
    the connexion itself, cursor creation and commit
    """

    def __init__(self):
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.passwrd = MYSQL_PASSWD
        self.database = MYSQL_DATABASE
        self.PurBeurreConnect = None

    def connect(self):
        """Connexion to MySQL using MySQL connector"""
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
        """Generate a cursor with the same connexion"""
        return self.PurBeurreConnect.cursor()

    def commit(self):
        """Generate a commit with the same connexion"""
        return self.PurBeurreConnect.commit()
