# Multi sections CSV flat file example

import io
import csv
from jsonschema import validate

# json schema https://json-schema.org
schema = {
    "$id": "https://example.com/person.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "header": {
            "type": "object",
            "csvTotalColumnNumber": 33,
            "properties": {
                "Type de fichier": {
                    "type": "string",
                    "csvColumn": 0
                },
                "Date de la commande": {
                    "type": "string",
                    "csvColumn": 2
                }
            }
        },
        "rows": {
            "type": "array",
            "items": {
                "type": "object",
                "csvTotalColumnNumber": 12,
                "properties": {
                    "Type de segment": {
                        "type": "string",
                        "csvColumn": 0
                    },
                    "Quantité unitaire": {
                        "type": "integer",
                        "csvColumn": 2
                    }
                }
            }
        }
    }
}

input_data = {
    "header": {
        "Type de fichier": "COMMANDE",
        "Date de la commande": "20221115"
    },
    "rows": [
        {
            "Type de segment": "LIGNE",
            "Quantité unitaire": 10
        },
        {
            "Type de segment": "LIGNE",
            "Quantité unitaire": 40
        }
    ]
}

validate(
    instance=input_data,
    schema=schema
)

output = io.StringIO()
writer = csv.writer(output, delimiter=';')
for section_name, section_data in input_data.items():
    if schema["properties"][section_name]["type"] == "object":
        tmp_row = [None] * schema["properties"][section_name]["csvTotalColumnNumber"]
        for field_name, field_params in schema["properties"][section_name]["properties"].items():
            tmp_row[field_params["csvColumn"]] = section_data[field_name]

        writer.writerow(tmp_row)

    elif schema["properties"][section_name]["type"] == "array":
        for input_row in section_data:
            tmp_row = [None] * schema["properties"][section_name]["items"]["csvTotalColumnNumber"]
            for field_name, field_params in schema["properties"][section_name]["items"]["properties"].items():
                tmp_row[field_params["csvColumn"]] = input_row[field_name]

            writer.writerow(tmp_row)

print(output.getvalue())
output.close()
