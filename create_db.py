# create_db.py
import mysql.connector

def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="charan123",
        database="billing_system"
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            meter_number VARCHAR(255) NOT NULL UNIQUE,
            amount_due FLOAT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
