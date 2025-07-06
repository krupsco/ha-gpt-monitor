import csv
import os

def log_data(state, timestamp):
    filepath = "data/history.csv"
    write_header = not os.path.exists(filepath)
    with open(filepath, mode="a", newline="") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["timestamp", "state"])
        writer.writerow([timestamp, state])

