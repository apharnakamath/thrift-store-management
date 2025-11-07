# Thrift-Store-Management-System

A simple database-driven application to manage customers, inventory, sales, donations, and employee performance in a thrift store. Built using MySQL and Python (Streamlit), this system helps streamline store operations with proper data integrity and real-time analytics.

## Features

* Customer registration & purchase history
* Inventory tracking with multiple storage locations
* Transaction processing
* Donation management with estimated values
* Employee performance analytics
* Low-stock alerts & reporting dashboard

## Tech Stack

* Database: MySQL 8.0+
* Frontend: Python Streamlit
* Language: SQL, Python
* Tools: MySQL Workbench, VS Code, Git/GitHub
  
## Installation & Setup

1. Clone the repository
```
git clone https://github.com/apharnakamath/thrift-store-management.git
cd thrift-store-management
```

2. Create the database
Open MySQL Workbench and execute:
```
CREATE DATABASE MINIPROJECT_DBMS;
USE MINIPROJECT_DBMS;
```

3. Import schema

Run the included mini-project.sql file.

4. Install dependencies

```
pip install streamlit pandas mysql-connector-python
```

5. Run the Streamlit app

```
streamlit run app.py
```

6. Enter your MySQL workbench password and connect to the database.
