
""" This module define application's parameters"""


import math

# MySQL Authentification
MYSQL_HOST = "localhost"
MYSQL_USER = "PBuser"
MYSQL_PASSWD = "ratatouille"
MYSQL_DATABASE = "dbPurBeurre"

# Products by categories
NB_PRODUCT = 20
PRODUCTS_PER_PAGE = 20

# Number of categories
NB_CATEGORIES = 5

NB_PAGES = math.ceil(NB_PRODUCT/PRODUCTS_PER_PAGE)
