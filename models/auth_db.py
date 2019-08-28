#! /usr/bin/env python3
# coding: utf-8

"""This module manage all operations on MySQL connexion"""

import mysql.connector
from models.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE


class DbAuth:
    """
    This class allowed to automate all operation on the connexion
    the connexion itself, cursor creation and commit
    """

    def __init__(self):
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.passwrd = MYSQL_PASSWD
        self.database = MYSQL_DATABASE
        self.pb_connect = None

    def connect(self):
        """Connexion to MySQL using MySQL connector"""
        try:
            self.pb_connect = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwrd,
                )
        except mysql.connector.errors.InterfaceError:
            print("Serveur MySQL inaccessible.")
            exit()

    def create_cursor(self):
        """Generate a cursor with the same connexion"""
        return self.pb_connect.cursor()

    def commit(self):
        """Generate a commit with the same connexion"""
        return self.pb_connect.commit()
