from app.client import SosClient
from app.config import Config, ConfigKey
import csv


def get_config_value(KEY):
    if not (Config.get(KEY)):
        value = input('%s: ' % KEY)
        Config.set(KEY, value)

    return Config.get(KEY)


client = SosClient(get_config_value(ConfigKey.URL))
candidates_data, fieldnames = client.get_candidates_data()

with open(get_config_value(ConfigKey.OUTPUT_FILE), 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(candidates_data)
