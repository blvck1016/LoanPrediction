import mysql.connector

def create_connection():
   
    mysql_host = 'medproject.mysql.database.azure.com'
    mysql_port = 3306 
    mysql_user = 'ifmpwbxopa@medproject'
    mysql_password = '1VRSAF7B6311Z1TV$'
    mysql_db = 'apploan-database'

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
