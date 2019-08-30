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

### I. Create a MySQL connexion :

This program use MySQL.connetor as interface
* **DbAuth** in auth_db.py module :
<br/>To ensure all MySQL requests would be using the app credentials, a **DbAuth** class creates specified connector (**connect()**), cursor(**create_cursor()**) and commit(**commit()**).  

### II. Get datas from Open Food Facts API into json files :

The programm uses two classes to do so :
* **JsonAPI** in json_api.py module :
<br/>An instance of this class launches url requests to the API and stores datas in json files in a '/data' repository
* **SortedDatas** in sort_datas.py module
<br/>An instance of this class filters datas before and after getting datas from the API.

#### Load datas ?
1. Method **check_first()** from **JsonAPI** :
<br/>Program checks first if datas already had been loaded in the project in the '/data' folder.
This method allows to create a condition to initialise API requests and MySQL tables creation

#### Get wanted categories from OFF
2. Method **get_categories()** from **JsonAPI** :
<br/>This method use HTTP library requests to get categories' informations from the API and save it in a 'data/categories.json' file
3. Method **filtered_categories()** from **SortedDatas** :
<br/>Once we have all categories datas, this method read them and keep only the number of categories defined in the **config.py** module. A 'final_cat' list is created in order to insert datas in database.
4. Method **get_info_from_categories()** from **SortedDatas** :
<br/>This method gets names and url names in a dictionnary. Names will be used to name json products files' and url names will be needed for API's requests.

#### Get wanted products from OFF
5. Method **get_products()** from **JsonAPI** :
<br/>With categories datas we've got with the previous method, we are able to send HTTP requests. We decided to limit products to french purchase places as final users should mostly be french. Requests will use number of pages and number per page specified in the **config.py** module. All those pages are saved in json files in the folder '/data'.
6. Method **filtered_products()**  from **SortedDatas** :
<br/>Now we have datas in json files we need to get datas from them in order to insert them in the database. Two lists are created. One is keeping the wanted datas from products such as id, name, brands... The other will keep for each product, the categories list referencing the product. We'll see later on we'll create a specific table in the database to link each product to the several categories it could be related.
7. Method **truncate_datas()** from **SortedDatas** :
<br/>Each of **filtered_categories()** and **filtered_products()** methods use it to truncate datas to fit th sizes we will define for MySQL tables.

### III. Create and fill MySQL tables :

The programm uses two classes to do so :
* **DbCreate** in create_db.py module :
<br/>An instance of this class create tables in the database
* **DbInsert** in insert_db.py module
<br/>An instance of this class insert sorted datas in the database

Those two classes takes an instance of the class **DbAuth** in argument to get the right connexion with MySQL Connector.

#### Create database structure
8. Method **drop()** from **DbCreate** :
<br/>First of all we have to ensure we won't add datas in already filled database. This method will reinitiate it.
9. Method **create_tables()** from **DbCreate** :
<br/>We create our tables.
To see the database's model, click [here](https://github.com/MayBaMay/PB_P5/blob/master/Modèle_Pur_Beurre.pdf).

#### Insert categories and products datas in database

10. Method **insert_categories()** from **DbInsert** :
<br/>With sorted datas from **SortedDatas** attribute **final_cat**, we insert categories
11. Method **insert_products()** from **DbInsert** :
<br/>With sorted datas from **SortedDatas** attribute **products_infos_list**, we insert products

#### Get products and categories relation
12. Method **get_categories_per_product()** from **SortedDatas** :
<br/>As we said earlier, each product can be related to several categories and a category is mostly composed to several products. We need to get those relations in a list to be able to insert them in the database. Using again our **DbAuth** object, we can store those relations in a list.

#### Insert links between products and categories in the specific table
13. Method **insert_prod_cat()** from **DbInsert** :
<br/>With sorted datas from **SortedDatas** attribute **asso**, we can insert datas.

### IV. User interface and database's interactions

The programm uses two classes to do so :
* **Print** in print.py module
<br/>This class constains only static methods and consolidate main interaction with the user in a specific module.

* **DbRead** in read_db.py module :
<br/>An instance of this class allows program to interact with the database and treats user inputs gotten from the **Print** class

14. User interface ==> class **Print** :

    Method **menu()** :
Display main menu
1 - Find a product and its alternative
2 - Display my watchlist
3 - Quit

    Method **category_choice()** :
Display menu categories
User choose a number of category
or 'F' to filter the research with a keyword
or '-1' to see categories list and choose an other one
or '0' to come back to main menu

    Method **product_choice()** :
Display menu Produits
User choose the number of a product
or 'F' to filter the research with a keyword
or '-1' to see categories list and choose an other one
or '0' to come back to main menu

    Method **keyword_research()** :
Asks user to enter keyword for a keyword research
user enter a keyword
or '-1' to see categories list and choose an other one
or '0' to come back to main menu

    Method **prod_not_in_category()** :
In case the chosen product doesn't belong to the chosen category, asks user's confirmation if he/she wants to display categories list or choose an other product number

    Method **prod_not_in_category()** :
Asks user's confirmation if he/she wants to display categories list
