# db_utils.py

import mysql.connector

def create_connection():
    # Replace these values with your Azure MySQL connection details
    mysql_host = 'projet.mysql.database.azure.com'
    mysql_port = 3306 
    mysql_user = 'med@projet'
    mysql_password = 'root@2002'
    mysql_db = 'projet'

    return mysql.connector.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
    )

def create_loan_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loan_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_no VARCHAR(255),
            full_name VARCHAR(255),
            prediction INT
        )
    """)
    connection.commit()

def insert_loan_data(connection, account_no, fn, prediction):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO loan_data (account_no, full_name, prediction)
        VALUES (%s, %s, %s)
    """, (account_no, fn, prediction))
    connection.commit()
