import json
import csv
from pathlib import Path
#File location
json_file = Path(__file__).parent.parent.parent / "testdata" / "test_results.json"
csv_file = Path(__file__).parent.parent.parent / "testdata" / "failed_tests.csv"

def read_results(json_file):
    """
    Read JSON test results.
    Handles malformed records using try/except.
    """
    valid_records = []

    try:
        with open(json_file, "r") as file:
            data = json.load(file)

        for record in data:
            try:
                valid_records.append({
                    "id": record["id"],
                    "name": record["name"],
                    "status": record["status"],
                    "duration_ms": record["duration_ms"],
                    "error_message": record["error_message"]
                })
            except KeyError as e:
                print(f"Skipping record due to missing key: {e}")

    except FileNotFoundError:
        print(f"File '{json_file}' not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")

    return valid_records

def filter_failed_tests(records):
    """
    Return only failed test records.
    """
    failed_records = []

    for record in records:
        try:
            if record["status"].lower() == "fail":
                failed_records.append(record)
        except KeyError as e:
            print(f"Missing key while filtering: {e}")

    return failed_records


def write_failed_tests_to_csv(records, csv_file):
    """
    Write failed test records to CSV.
    """
    try:
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(
                ["id", "name", "error_message", "duration_ms"]
            )

            for record in records:
                writer.writerow([
                    record["id"],
                    record["name"],
                    record["error_message"],
                    record["duration_ms"]
                ])

        print(f"CSV file created: {csv_file}")

    except Exception as e:
        print(f"Error writing CSV: {e}")


if __name__ == "__main__":

    test_records = read_results(json_file)

    failed_tests_data = filter_failed_tests(test_records)

    # List comprehension to extract failed test IDs
    failed_test_ids = [
        test["id"]
        for test in failed_tests_data
    ]

    print("Failed Test IDs:", failed_test_ids)
    print("Failed Test Count:", len(failed_test_ids))

    write_failed_tests_to_csv(
        failed_tests_data,
        csv_file
    )