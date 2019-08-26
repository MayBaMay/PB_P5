
import math

# MySQL Authentification
MYSQL_HOST = "localhost"
MYSQL_USER = "maylis"
MYSQL_PASSWD = "ratatouille"
MYSQL_DATABASE = "dbPurBeurre"

# Products by categories
NB_PRODUCT = 50
PRODUCTS_PER_PAGE = 50

# Number of categories
NB_CATEGORIES = 20

NB_PAGES = math.ceil(NB_PRODUCT/PRODUCTS_PER_PAGE)
