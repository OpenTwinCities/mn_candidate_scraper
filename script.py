from app.client import SosClient
from app.config import Config, ConfigKey
import csv


def get_config_value(KEY):
    if not (Config.get(KEY)):
        value = input('%s: ' % KEY)
        Config.set(KEY, value)

    return Config.get(KEY)


client = SosClient(get_config_value(ConfigKey.URL))
candidate_datas, fieldnames = client.get_candidate_data()

with open(get_config_value(ConfigKey.OUTPUT_FILE), 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(candidate_datas)

# 1. GET https://candidates.sos.state.mn.us/CandidateFilingResults.asp
# 2. Find table
# 3. Loop through trs. For each with a `style=height:30px;`:
#    1. note the district
#    2. Loop through following trs until another one with style marker. For each with a class of `evenRow` or `oddrow`:
#       1. POST to CandidateFilingResults URL and provide id associated with link
#       2. Follow redirect to GET candiate's filing page
#       3. Find table within table
#       4. Find all span elements within this table. For each
#          1. Note the text in the span as a value
#          2. Find the cooresponding TD in the previous TR. Note this as the key, and add to the set of keys
# 4. Write list of dictionaries to a CSV, using the set of keys
