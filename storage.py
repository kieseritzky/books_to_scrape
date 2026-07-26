import csv, json


def save_to_csv(filename, data, fieldnames):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Succesfully saved CSV to {filename}")

def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f" Successfully saved JSON to {filename}")