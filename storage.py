import json
import os

FILE_NAME = "data.json"

def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def add_transaction(transaction):
    data = load_data()
    data.append(transaction.to_dict())
    save_data(data)