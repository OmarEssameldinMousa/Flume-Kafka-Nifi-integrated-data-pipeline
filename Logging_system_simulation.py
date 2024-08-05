import time 
import random
import datetime

log_file_path = "logs.txt"

severity_levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]

# sample Log message
 
messages = [
    "User login successful",
    "User login failed",
    "File not found",
    "Connection timed out",
    "Data successfully processed",
    "Error processing data",
] 

def generate_log_entry():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    severity = random.choice(severity_levels)
    message = random.choice(messages)
    log_entry = f"{timestamp} - {severity} - {message}"
    return log_entry

def simulate_logging():
    with open(log_file_path, "a") as log_file:
        while True:
            log_entry = generate_log_entry()
            log_file.write(log_entry + "\n")
            time.sleep(1)

if __name__ == "__main__":
    try:
        print("Logging simulation started. Press Ctrl+C to stop")
        simulate_logging()
    except KeyboardInterrupt:
        print("Logging simulation stopped")