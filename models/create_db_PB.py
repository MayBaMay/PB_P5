#! /usr/bin/env python3
# coding: utf-8

"""
This module manage creation of tables database.
"""

import mysql.connector

from models.config import *


class DbCreate:
    """
    Create database and tables structure.
    """

    def __init__(self, dbauth):
        self.connect = dbauth


    def create_tables(self):
        """
        Create MySQL tables in dbPurBeurre database.
        """
        cursor = self.connect.create_cursor()
        cursor.execute("USE `dbPurBeurre`")

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `dbPurBeurre`.`Categories` ("
            "   `num` INT UNSIGNED AUTO_INCREMENT,"
            "   `id` VARCHAR(80) NOT NULL,"
            "   `name` VARCHAR(80) NOT NULL,"
            "   `url` VARCHAR(255) NOT NULL,"
            "   `products` INT NULL,"
            "   PRIMARY KEY (`num`))"
            "   ENGINE = InnoDB"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `dbPurBeurre`.`Produits` ("
            "   `id` VARCHAR(80) NOT NULL,"
            "   `product_name` VARCHAR(80) NOT NULL,"
            "   `nutrition_grade_fr` CHAR(1) NOT NULL,"
            "   `brands` VARCHAR(80) NULL,"
            "   `stores` VARCHAR(80) NOT NULL,"
            "   `url` VARCHAR(255) NOT NULL,"
            "   `favoris` DATE NULL,"
            "   PRIMARY KEY (`id`))"
            "   ENGINE = InnoDB"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `dbPurBeurre`.`Asso_Prod_Cat` ("
            "   `num_categories` INT UNSIGNED,"
            "   `id_produits` VARCHAR(80) NOT NULL,"
            "   PRIMARY KEY (`num_categories`, `id_produits`),"
            "   CONSTRAINT `fk_num_categories`"
            "       FOREIGN KEY (`num_categories`)"
            "       REFERENCES `Categories` (`num`),"
            "   CONSTRAINT `fk_id_produits`"
            "       FOREIGN KEY (`id_produits`)"
            "       REFERENCES `Produits` (`id`))"
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
            ("DROP TABLE IF EXISTS Asso_Prod_Cat"),
            ("DROP TABLE IF EXISTS Categories"),
            ("DROP TABLE IF EXISTS Produits")
        )

        for query in queries:
            cursor.execute(query)
