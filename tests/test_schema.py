from pyroll.from_dict.schema import create_schema
import pyroll.core as pr
from rich import print


# def test_schema_transport():
#     create_schema(pr.Transport)
def test_schema_profile():
    schema = create_schema(pr.Profile, pr.Profile.round)

    print(schema.json_schema("test/profile"))


def test_schema_roll_pass():
    schema = create_schema(pr.RollPass, pr.RollPass)

    print(schema.json_schema("test/roll_pass"))
