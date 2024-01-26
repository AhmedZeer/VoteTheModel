import csv
import os

my_path = "mGPT.csv"


def load_data(path):
    data = []
    with open( path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

data = load_data(my_path)
print(data[0]['cvp'])
