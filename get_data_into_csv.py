import mysql.connector
from mysql.connector import Error
import csv
import time

# i have written this code to fetch data from mysql database and write it to csv file without using multiprocessing to fetch data faster

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user= user_name,
            passwd=user_password,
            database=db_name
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def fetch_data(connection, query, csv_file_path):
    cursor = connection.cursor()
    try:
        start_time = time.time()
        cursor.execute(query)
        rows = cursor.fetchall()
        header= [i[0] for i in cursor.description]
        end_time = time.time()
        print(f"Time taken to fetch data: {end_time - start_time:.2f} seconds")

        with open(csv_file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        
        print(f"Data successfully written to {csv_file_path}")

    except Error as e:
        print(f"The error '{e}' occurred")
    
    cursor.close()
    

if __name__ == "__main__":
    host = 'localhost'
    user = 'usernmae'
    password = '********'
    database = 'database_name'
    csv_file_path = './users.csv'
    conn = create_connection(host, user, password, database)
    if conn:
        query = 'SELECT * FROM users'
        fetch_data(conn, query, csv_file_path)
        conn.close()