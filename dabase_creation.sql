
""" Script de création MySQL de la base de donnée Pur Beurre """


Mysql -h localhost -u root -p
# insert root password

CREATE USER 'PBuser'@'localhost' IDENTIFIED BY 'ratatouille';
GRANT ALL PRIVILEGES ON dbPurBeurre.* TO 'PBuser'@'localhost';

EXIT
