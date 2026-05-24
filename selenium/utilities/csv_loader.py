import csv
import os

def load_test_data(file_name="test_data.csv"):
    data = []
    # Adjust path to tests_data folder
    base_dir = os.path.dirname(os.path.dirname(__file__))  # project root
    file_path = os.path.join(base_dir, "test_data", file_name)

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data
