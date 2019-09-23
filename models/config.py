
""" This module defines application's parameters"""


import math

# MySQL Authentification
MYSQL_HOST = "localhost"
MYSQL_USER = "PBuser"
MYSQL_PASSWD = "ratatouille"
MYSQL_DATABASE = "dbPurBeurre"

# Products by categories
NB_PRODUCT = 200
PRODUCTS_PER_PAGE = 100
NB_PAGES = math.ceil(NB_PRODUCT/PRODUCTS_PER_PAGE)

# Number of categories
NB_CATEGORIES = 20

# Minimum number of products in a categorie to use it in app
MINPRODINCAT = 10000
