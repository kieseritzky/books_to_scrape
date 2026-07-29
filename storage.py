import csv, json
from logger_config import logging

logger = logging.getLogger(__name__)

def save_to_csv(filename, data, fieldnames):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    logger.info("Successfully saved CSV to %s", filename)

def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    logger.info("Successfully saved JSON to %s", filename)
