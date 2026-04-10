import json
from jsonschema import validate

with open("signal_schema.json") as f:
    SCHEMA = json.load(f)


def validate_signal(signal):
    validate(instance=signal, schema=SCHEMA)
    return True