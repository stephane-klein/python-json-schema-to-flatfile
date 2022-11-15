# Mono section CSV flat file
import io
import csv
import pprint

# json schema https://json-schema.org
schema = {
    "$id": "https://example.com/person.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "Type de fichier": {
            "type": "string",
            "csvColumn": 0
        },
        "Type de mouvement": {
            "type": "string",
            "csvColumn": 1
        },
        "Code": {
            "type": "integer",
            "csvColumn": 2
        }
    }
}

input_data = """
MV;LV;1234;20221115113620;32;20221120;;;;;;;;;;;
MV;SO;1888;20221115113620;32;20221120;;;;;;;;;;;
"""

input_io = io.StringIO(input_data)
csvreader = csv.reader(input_io, delimiter=";")

output_data = []
for row in csvreader:
    if len(row) > 0:
        tmp_output_row = {}
        for field_name, field_params in schema["properties"].items():
            tmp_output_row[field_name] = row[field_params["csvColumn"]]

        output_data.append(tmp_output_row)

pprint.pprint(output_data)
