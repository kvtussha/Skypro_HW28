import csv
import json
from config import Config


def csv_to_json(csv_file_path, json_file_path):
    json_data = []


    with open(csv_file_path, encoding='utf-8') as csvf:
        csvreader = csv.DictReader(csvf)
        for row in csvreader:
            row_keys = [x.lower() for x in list(row.keys())]
            new_row = dict(zip(row_keys, list(row.values())))
            json_data.append(new_row)

    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        json_file = json.dumps(json_data, indent=4, ensure_ascii=False)
        jsonf.write(json_file)


csv_to_json(Config.AD_PATH_CSV, Config.AD_PATH_JSON)
csv_to_json(Config.CATEGORY_PATH_CSV, Config.CATEGORY_PATH_JSON)
csv_to_json(Config.LOCATION_PATH_CSV, Config.LOCATION_PATH_JSON)
csv_to_json(Config.USER_PATH_CSV, Config.USER_PATH_JSON)
