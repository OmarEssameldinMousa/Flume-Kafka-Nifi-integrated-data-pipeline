# Dummy Project

## Project Overview

This project demonstrates data ingestion using batch processing and real-time streaming. It includes generating user data, importing it into a Hadoop Distributed File System (HDFS), and simulating a real-time logging system.

## Architecture

![Blank diagram](https://github.com/user-attachments/assets/cf345ddf-bd97-4dd4-9656-ea32d9cd0490)


### Batch Streaming

1. **Data Generation and Storage:**
   - **MariaDB:** Stores user data.
   - **HDFS:** Stores imported user data for batch processing.

     ```sql
       CREATE TABLE users (
          user_id INT AUTO_INCREMENT PRIMARY KEY,
          username VARCHAR(50) NOT NULL UNIQUE,
          email VARCHAR(100) NOT NULL UNIQUE,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
     ```

2. **Data Flow:**
   - **Data Generation:** Uses `faker` to create unique user data with multiprocessing for performance.
   - **Data Import:** Utilizes Apache Sqoop to import data from MariaDB to HDFS. Additionally, a custom script exports data from MariaDB to CSV as an alternative to Sqoop.

### Real-Time Streaming

1. **Logging System Simulator:**
   - Generates log data in real-time using a script that creates log entries.

2. **Data Flow:**
   - **Apache NiFi:** Ingests logs and routes data.
   - **Apache Kafka:** Acts as a message broker.
   - **Apache Flume:** Agents collect, aggregate, and move log data.
   - **HDFS:** Stores processed log data for analysis.

## Implementation

### 1. Schema Development

- **MariaDB Schema:**
  - `id`: Auto-increment
  - `username`: Unique
  - `email`: Unique
  - `created_at`: Timestamp (default current timestamp)

### 2. Data Generation

- **Script 1 (Single-process):**
  - Generates random user data using `faker`.

- **Script 2 (Multiprocessing):**
  - Enhances data generation performance by leveraging multiple CPU cores.
  - Ensures uniqueness constraints for `username` and `email`.

### 3. Data Import

- **Using Apache Sqoop:**
  - Imports data from MariaDB to HDFS.
  - ```sh
    sqoop import --connect jdbc:mysql://localhost:3306/yourdb --username yourusername --password yourpassword --table yourtable --target-dir /user/hadoop/yourtable
    ```

- **Custom CSV Export Script:**
  - Reads data from MariaDB and saves it as a CSV file without using Sqoop.
  

### 4. Real-Time Streaming

#### Logging System Simulator

- Simulates log data in real-time using a script that generates log entries.

#### Data Pipeline

1. **Apache NiFi Configuration:**
   - Ingest logs and route data:
     - Create a Kfka consumer processor to read log files.
     - creating a AlterText processor to add a colon to the end of each log info.
     - creating PutFile processor and PutHDFS processor
       
       ```xml
         will be published soon

       ```

2. **Apache Kafka Configuration:**
   - Create a Kafka topic to hold log data:
     ```sh
     kafka-topics --create --topic logs --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```

3. **Apache Flume Configuration:**
   - Configure Flume agents to collect and aggregate log data:
     - **Flume Agent 1 Configuration:**
       ```properties
         a1.sources = r1
         a1.channels = c1
         a1.sinks = kafkaSink
         
         a1.sources.r1.type = exec
         a1.sources.r1.command = tail -F /home/student/flume2/server_logging_system/logs/logs.txt
         
         a1.sinks.kafkaSink.type = org.apache.flume.sink.kafka.KafkaSink
         a1.sinks.kafkaSink.flumeBatchSize = 1
         a1.sinks.kafkaSink.kafka.bootstrap.servers = localhost:9092
         a1.sinks.kafkaSink.kafka.topic = project_test_topic
         
         # Use a channel which buffers events in memory
         a1.channels.c1.type = memory
         a1.channels.c1.capacity = 1000
         a1.channels.c1.transactionCapacity = 100
         
         # Bind the source and sink to the channel
         a1.sources.r1.channels = c1
         a1.sinks.kafkaSink.channel = c1
       ```

     - **Flume Agent 2 Configuration:**
       ```properties
         a2.sources = r1
         a2.channels = c1
         a2.sinks = kafkaSink
         
         a2.sources.r1.type = exec
         a2.sources.r1.command = tail -F /home/student/flume2/server_logging_system/logs/logs2.txt
         
         a2.sinks.kafkaSink.type = org.apache.flume.sink.kafka.KafkaSink
         a2.sinks.kafkaSink.flumeBatchSize = 1
         a2.sinks.kafkaSink.kafka.bootstrap.servers = localhost:9092
         a2.sinks.kafkaSink.kafka.topic = project_test_topic
         
         # Use a channel which buffers events in memory
         a2.channels.c1.type = memory
         a2.channels.c1.capacity = 1000                                                                                                                                 
         a2.channels.c1.transactionCapacity = 100                                                                                                                       
                                                                                                                                                                        
         # Bind the source and sink to the channel                                                                                                                      
         a2.sources.r1.channels = c1                                                                                                                                    
         a2.sinks.kafkaSink.channel = c1                                                                                                                                
     
       ```

## Challenges and Solutions

- **Ensuring Data Uniqueness:**
  - Implemented checks to maintain unique `username` and `email`.
  
- **Performance Optimization:**
  - Used multiprocessing for efficient data generation.

- **Debugging and Error Handling:**
  - Implemented robust logging and error-handling mechanisms.

## Conclusion

This project integrates batch processing and real-time streaming to provide a comprehensive learning experience in data ingestion. By following the documented architecture and implementation steps, you can recreate and understand the project's data processing pipelines.

