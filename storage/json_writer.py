import csv, json, logging

logger = logging.getLogger(__name__)

def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    logger.info("Successfully saved JSON to %s", filename)
