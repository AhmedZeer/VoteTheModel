import csv

def append_to_csv(file_path, data):
    """
    Appends data to a CSV file.

    Parameters:
        - file_path (str): Path to the CSV file.
        - data (list): List of dictionaries representing rows to be appended.

    Example:
        append_to_csv('example.csv', [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}])
    """
    # Check if the file exists, create it with headers if not
    file_exists = os.path.exists(file_path)
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = data[0].keys() if data else []
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write headers only if the file was just created
        if not file_exists:
            csv_writer.writeheader()

        # Append data to the CSV file
        csv_writer.writerows(data)

# Example usage:
file_path = 'example.csv'
data_to_append = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
append_to_csv(file_path, data_to_append)
