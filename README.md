# Find a substitute with Open Food Facts

This application was conceived to help consumer to find healthy alternatives.
<br/>It uses [Open Food Facts API](https://world.openfoodfacts.org])

## How it works :

Make sure your environnement runs requirements

You need to create a MySQL user and give privileges to him on dbPurBeurre database.
```mysql
Mysql -h localhost -u root -p
# insert your root password

CREATE USER 'PBuser'@'localhost' IDENTIFIED BY 'ratatouille';
GRANT ALL PRIVILEGES ON dbPurBeurre.* TO 'PBuser'@'localhost';

EXIT
```
Those credentials are contained in config.py module and will be used by the application.
