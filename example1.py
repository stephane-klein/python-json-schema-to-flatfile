import io
import csv
from jsonschema import validate

# json schema https://json-schema.org
schema = {
    "$id": "https://example.com/person.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "csvTotalColumnNumber": 30,
    "properties": {
        "Type de message": {
            "type": "string",
            "maxLength": 3,
            "csvColumn": 1
        },
        "Description": {
            "type": "string",
            "maxLength": 100,
            "csvColumn": 5
        },
        "Nombre de colis par unité logistique": {
            "type": "integer",
            "maximum": 9999999999,
            "csvColumn": 16
        },
        "Hauteur du colis de référence": {
            "type": "number",
            "maximum": 999999999,
            "multipleOf": 0.001,
            "csvColumn": 19
        },
        "Poids net du colis de référence": {
            "type": "number",
            "maximum": 999999999,
            "multipleOf": 0.001,
            "csvColumn": 25
        }
    }
}

input_data = {
    "Type de message": "ART",
    "Description": "Description 1",
    "Hauteur du colis de référence": 12.112,
    "Poids net du colis de référence": 405.009,
    "Nombre de colis par unité logistique": 123421
}

validate(
    instance=input_data,
    schema=schema
)

row = [None] * schema["csvTotalColumnNumber"]
for field_name, field_params in schema["properties"].items():
    row[field_params["csvColumn"] - 1] = input_data[field_name]

output = io.StringIO()
writer = csv.writer(output, delimiter=';')
writer.writerow(row)
print(output.getvalue())
output.close()
