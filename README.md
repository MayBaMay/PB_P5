# Find a substitute with Open Food Facts

This application was conceived to help consumer to find healthy alternatives.
<br/>For now, you can run it on your terminal as it hasn't been programmed with a graphic interface.
<br/>It uses [Open Food Facts API](https://world.openfoodfacts.org])

## How to use it :

Make sure your environnement runs requirements

You need to create a MySQL user 'PBuser' and give privileges to him on 'dbPurBeurre' database.
```mysql
Mysql -h localhost -u root -p
# insert your root password

CREATE USER 'PBuser'@'localhost' IDENTIFIED BY 'ratatouille';
GRANT ALL PRIVILEGES ON dbPurBeurre.* TO 'PBuser'@'localhost';

EXIT
```
Those credentials are contained in config.py module and will be used by the application.

To launch the program, run in your terminal:
```bash
Python3 pur_beurre.py
```

## How it works :

### Get datas from Open Food Facts API into json files :

The programm uses two classes to do so :
* **JsonAPI** in json_api.py module :
<br/>This module launches url requests to the API and stores datas in json files in a '/data' repository  
* **SortedDatas** in sort_datas.py module
<br/>This module filters datas before and after getting datas from the API.


1. Method **check_first()** from **JsonAPI**
Program checks first if datas already had been loaded in the project in the '/data' folder.
This method allows to create a condition to initialise API requests and MySQL tables creation
2. Method **get_categories()** from **JsonAPI**
If
