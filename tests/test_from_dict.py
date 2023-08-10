from pyroll.input_text.from_dict import from_dict
from tests.conf import D_IN_PROFILE, check_in_profile, D_UNIT, check_unit


def test_in_profile():
    p = from_dict(D_IN_PROFILE, {})
    check_in_profile(p)


def test_unit():
    u = from_dict(D_UNIT, {})
    check_unit(u)
