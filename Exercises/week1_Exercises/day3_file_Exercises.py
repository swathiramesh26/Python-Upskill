import csv
import json
file_path_csv="testdata/users.csv"
file_path_json="testdata/users.json"

# Read CSV data
def read_csv_data(file_path_csv):
    print("\nReading CSV Data")

    with open(file_path_csv, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                print(f"username: {row['username']}")
                print(f"password: {row['password']}")
            except KeyError as e:
                print(f"Missing key: {e}")
            print("-" * 20)


# Read JSON data
def read_json_data(file_path_json):
    print("\nReading JSON Data")

    with open(file_path_json, "r") as file:
        data = json.load(file)

        for user in data:
            try:
                username = user["username"]
                print(f"Username: {username}")
                password = user["password"]
                print(f"Password: {password}")

            except KeyError as e:
                print(f"Missing key: {e}")

            print("-" * 20)


# Main program
read_csv_data(file_path_csv)
read_json_data(file_path_json)
