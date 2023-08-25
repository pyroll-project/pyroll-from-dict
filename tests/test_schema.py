import json
from pathlib import Path

from pyroll.from_dict.schema import create_schema, create_input_schema
import pyroll.core as pr
from rich import print_json

THIS_DIR = Path(__file__).parent


# def test_schema_transport():
#     create_schema(pr.Transport)
def test_schema_profile():
    schema = create_schema(pr.Profile, pr.Profile.round)

    json_schema = json.dumps(schema.json_schema("test/profile"))

    print_json(json_schema)
    (THIS_DIR / "profile.schema.json").write_text(json_schema)

    json_data = (THIS_DIR / "profile.json").read_text()

    data = json.loads(json_data)

    schema.validate(data)


def test_schema_roll_pass():
    schema = create_schema(pr.RollPass, pr.RollPass)

    json_schema = json.dumps(schema.json_schema("test/roll_pass"))

    print_json(json_schema)
    (THIS_DIR / "roll_pass.schema.json").write_text(json_schema)

    json_data = (THIS_DIR / "roll_pass.json").read_text()

    data = json.loads(json_data)

    schema.validate(data)


def test_input_schema():
    schema = create_input_schema()

    json_schema = json.dumps(schema.json_schema("test/input", use_refs=True))

    print_json(json_schema)
    (THIS_DIR / "input.schema.json").write_text(json_schema)

    json_data = (THIS_DIR / "input.json").read_text()

    data = json.loads(json_data)

    schema.validate(data)
