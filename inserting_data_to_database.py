import mysql.connector
from mysql.connector import Error
from faker import Faker
from multiprocessing import Process, Manager, Lock
import time

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def generate_unique_data(existing_dict, generator_function, lock):
    while True:
        unique_value = generator_function()
        with lock:
            if unique_value not in existing_dict:
                existing_dict[unique_value] = None
                return unique_value

def execute_query(connection, cursor, query, data):
    try:
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")

def insert_users_data(existing_usernames, existing_emails, lock):
    host = 'localhost'
    user = 'username'
    password = '******'
    database = 'TEST'
    conn = create_connection(host_name=host, user_name=user, user_password=password, db_name=database)
    fake = Faker()
    if conn:
        cursor = conn.cursor()
        for _ in range(1000):
            username = generate_unique_data(existing_usernames, fake.user_name, lock)
            email = generate_unique_data(existing_emails, fake.email, lock)
            query = 'INSERT INTO users (username, email) VALUES (%s, %s)'
            execute_query(conn, cursor, query, data=(username, email))
        cursor.close()
        conn.close()



if __name__ == "__main__":
    number_of_threads = 10
    processes = []
    start_time = time.time()

    with Manager() as manager:
        existing_usernames = manager.dict()
        existing_emails = manager.dict()
        lock = Lock()
        for _ in range(number_of_threads):
            process = Process(target=insert_users_data, args=(existing_usernames, existing_emails, lock))
            processes.append(process)

        for process in processes:
            process.start()

        
        for process in processes:
            process.join()

    end_time = time.time()
    print("All processes are done")
    print("Data inserted successfully")
    print(f"Time taken: {end_time - start_time}")


