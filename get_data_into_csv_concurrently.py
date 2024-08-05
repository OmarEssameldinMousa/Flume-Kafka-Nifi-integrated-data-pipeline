import mysql.connector
from mysql.connector import Error
from multiprocessing import Process, Manager, Lock
import math
import time
import pandas as pd

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def fetch_data_chunk(host, user, password, database, query, offset, limit, result_list, lock, header_list):
    connection = create_connection(host, user, password, database)
    if not connection:
        return

    cursor = connection.cursor()
    try:
        paginated_query = f"{query} LIMIT {limit} OFFSET {offset}"
        cursor.execute(paginated_query)
        rows = cursor.fetchall()

        with lock:
            if not header_list:  # Only add headers once
                header_list.append([i[0] for i in cursor.description])
            result_list.extend(rows)
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

# def write_data_to_csv(headers, data, csv_file_path):
#     with open(csv_file_path, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(headers)  # Write headers
#         writer.writerows(data)    # Write data
#     print(f"Data successfully written to {csv_file_path}")

def write_data_to_csv(headers, data, csv_file_path):
    df = pd.DataFrame(list(data), columns=headers)
    df.to_csv(csv_file_path, index=False)
    print(f"Data successfully written to {csv_file_path}")


if __name__ == "__main__":
    host = 'localhost'
    user = 'username'
    password = '********'
    database = 'database_name'
    query = 'SELECT * FROM users'  # Your query here
    csv_file_path = 'users_data.csv'
    
    # Create a connection to calculate the total number of rows
    conn = create_connection(host, user, password, database)
    if not conn:
        exit("Failed to create database connection.")
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM ({query}) AS total")
    total_rows = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    num_chunks = 10  # Number of chunks/processes
    limit = math.ceil(total_rows / num_chunks)  # Number of rows per chunk
    manager = Manager()
    result_list = manager.list()
    header_list = manager.list()
    lock = Lock()
    
    start_time = time.time()
    processes = []
    for i in range(num_chunks):
        offset = i * limit
        process = Process(target=fetch_data_chunk, args=(host, user, password, database, query, offset, limit, result_list, lock, header_list))
        processes.append(process)
        process.start()

    end_time = time.time()

    print(f"Time taken to fetch data : {end_time - start_time} second")

    start_time = time.time()
    
    for process in processes:
        process.join()
        
    end_time = time.time()
    print(f"Time taken to join the processes to the main program data : {end_time - start_time} second")


    start_time = time.time()

    if header_list:
        write_data_to_csv(header_list[0], result_list, csv_file_path)
    end_time = time.time()
    
    print(f"Time taken to write data : {end_time - start_time} second")

    # Write data to CSV
    print("All processes are done")
    print("Data inserted successfully")


# from this experiment i can see a significant improvement in the time taken to fetch data from the database only but the time taken to write the data to the csv file has got worse 