import os
BASE_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(BASE_DIR, "signal_schema.json")

with open(SCHEMA_PATH) as f:
    SCHEMA = json.load(f)


def validate_signal(signal):
    validate(instance=signal, schema=SCHEMA)
    return True