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
Those credentials are contained in **config.py** module and will be used by the application.

To launch the program, run in your terminal:
```bash
Python3 pur_beurre.py
```

## How it works :

### Create a MySQL connexion :

* **DbAuth** in auth_db.py module :
<br/>To ensure all MySQL requests would be using the app credentials, a **DbAuth** class creates specified connector (**connect()**), cursor(**create_cursor()**) and commit(**commit()**).  

### Get datas from Open Food Facts API into json files :

The programm uses two classes to do so :
* **JsonAPI** in json_api.py module :
<br/>This module launches url requests to the API and stores datas in json files in a '/data' repository
* **SortedDatas** in sort_datas.py module
<br/>This module filters datas before and after getting datas from the API.

#### Load datas ?
1. Method **check_first()** from **JsonAPI** :
<br/>Program checks first if datas already had been loaded in the project in the '/data' folder.
This method allows to create a condition to initialise API requests and MySQL tables creation

#### Get wanted categories from OFF
2. Method **get_categories()** from **JsonAPI** :
<br/>This method use HTTP library requests to get categories' informations from the API and save it in a 'data/categories.json' file
3. Method **filtered_categories()** from **SortedDatas** :
<br/>Once we have all categories datas, this method read them and keep only the number of categories defined in the **config.py** module. We also chose to keep only categories with at least 10000 products in it. a 'final_cat' list is created in order to insert datas in database.
4. Method **get_info_from_categories()** from **SortedDatas** :
<br/>This method gets names and url names in a dictionnary. Names will be used to name json products files' names and url names will be needed for API's requests.

#### Get wanted products from OFF
5. Method **get_products()** from **JsonAPI** :
<br/>With categories info we've got with the last method, we are able to send HTTP requests. We decided to limit products to french purchase places as final users should mostly be french. Requests will use number of pages specified in the **config.py** module. All those pages are saved in  a json file in the folder '/data'.
6. Method **filtered_products()**  from **SortedDatas** :
<br/>Now we have datas in json files we need to get datas from them in order to insert them in the database. Two lists are created. One is keeping the wanted datas from products such as id, name, brands... The other will keep for each product, the categories list referencing the product. We'll see later on we'll create a specific table in the database to link each product to the several categories it could be related.
