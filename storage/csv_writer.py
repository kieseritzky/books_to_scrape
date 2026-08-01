import csv, json, logging

logger = logging.getLogger(__name__)

def save_to_csv(filename, data, fieldnames):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    logger.info("Successfully saved CSV to %s", filename)

