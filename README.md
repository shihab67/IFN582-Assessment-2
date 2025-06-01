# IFN582 Assessment 2

## Full-Developed Web Application

**Assessment 2 Features**
We have Developed **GROCS**, a grocery delivery web application, using **IFN582** workshop techniques. Features include:

- **Landing Page**: Product listing with search (by name) and category filter, using Bootstrap 5.3.
- **Item Details**: Product details with add-to-basket option.
- **Basket**: CRUD operations (add, update, delete, clear) in session, with dynamic totals.
- **Checkout**: Validated delivery form (name, email, address, phone, delivery option), emphasizing Delivery options like Click and Collect, Express and Eco-Friendly.
- **Access Management**: User login, registration, and admin panel for product management, category management and order management. Restricted admin access using custom decorators.
- **Error Handling**: Custom 404, 403 and 500 error pages.
- **Professional UI**: Responsive Bootstrap-Flask design, no form errors.
- **Sample Data**: 15 products, 2 categories, 6 users (2 admins, 4 customers), 3 orders across 3 different users with unique delivery option.

### How to setup the project

 1. Download the .zip folder or clone the repository from [here](https://github.com/shihab67/IFN582-Assessment-2.git), after cloning change the branch to **v2**. Then fetch.
 2. After downloading go to `project/__init__.py` file and update the following lines:
`app.config['SECRET_KEY']  =  'your-secret-key'
app.config['MYSQL_HOST']  =  'localhost'
app.config['MYSQL_USER']  =  'your-mysql-username'
app.config['MYSQL_PASSWORD']  =  'your-mysql-password'
app.config['MYSQL_DB']  =  'mysql-db-name'`
 3. Then create a database in **MySQL Workbench** using the same name then go to `project/database.sql` and copy the full SQL query and then run the query in your database.
 4. After database is successfully imported go to the project directory or in your **vscode** open the terminal and run `py  -m pip install -r requirements.txt` `python3  -m  pip  install  -r  requirements.txt` these commands.
 5. After all the necessary packages have been installed you can then start the project by running `python run.py`.
 6. By default the project will start on [http://127.0.0.1:8888](http://127.0.0.1:8888). Visit the link and view the project.

## Sample Data

### User credentials and roles

|Sl.|Email|Password|Role
|--|--|--|--
|1.|<admin@gmail.com>  |adminpass  |Admin
|2.|<admin2@gmail.com>  |adminpass  |Admin
|3.|<john@gmail.com>  |adminpass  |Customer
|4.|<jane@gmail.com>  |adminpass  |Customer
|5.|<alice@gmail.com>  |adminpass  |Customer
|6.|<bob@gmail.com>  |adminpass  |Customer
