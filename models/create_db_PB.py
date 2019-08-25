#! /usr/bin/env python3
# coding: utf-8

"""
This module manage MySQL database.
"""

import mysql.connector

from models.config import *


class DbCreate:
    """
    Create database and tables structure.
    """

    def __init__(self, dbauth):
        self.connect = dbauth

    def test_database(self):
        """
        Test if database is created
        """
        cursor = self.connect.create_cursor()
        cursor.execute(
            "SELECT SCHEMA_NAME "
            "FROM INFORMATION_SCHEMA.SCHEMATA "
            "WHERE SCHEMA_NAME = 'dbPurBeurre'"
        )
        return cursor

    def create_database(self):
        """
        Create database dbPurBeurre
        """
        cursor = self.connect.create_cursor()
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS dbPurBeurre "
            "CHARACTER SET utf8mb4 "
            "COLLATE utf8mb4_unicode_ci"
        )

    def create_tables(self):
        """
        Create MySQL tables in dbPurBeurre database.
        """
        cursor = self.connect.create_cursor()
        cursor.execute("USE `dbPurBeurre`")

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `dbPurBeurre`.`Categories` ("
            "   `num` INT NOT NULL AUTO_INCREMENT,"
            "   `id` VARCHAR(80) NOT NULL,"
            "   `name` VARCHAR(80) NOT NULL,"
            "   `url` VARCHAR(255) NOT NULL,"
            "   `products` INT NULL,"
            "   PRIMARY KEY (`num`))"
            "   ENGINE = InnoDB"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `dbPurBeurre`.`Produits` ("
            "   `num` INT NOT NULL AUTO_INCREMENT,"
            "   `id` VARCHAR(80) NOT NULL,"
            "   `product_name` VARCHAR(80) NOT NULL,"
            "   `nutrition_grade_fr` CHAR(1) NOT NULL,"
            "   `brands` VARCHAR(80) NULL,"
            "   `stores` VARCHAR(80) NOT NULL,"
            "   `url` VARCHAR(255) NOT NULL,"
            "   `id_categorie` VARCHAR(60) NOT NULL,"
            "   PRIMARY KEY (`num`))"
            "   ENGINE = InnoDB"
        )


    def drop(self):
        """
        Drop tables in dbPurBeurre.
        """
        cursor = self.connect.create_cursor()
        queries = (
            ("USE dbPurBeurre"),
            ("SET foreign_key_checks = 0"),
            ("DROP TABLE IF EXISTS Categories"),
            ("DROP TABLE IF EXISTS Produits")
        )

        for query in queries:
            cursor.execute(query)
