from pyroll.from_dict.from_dict import from_dict, dict_input
from tests.conf import D_IN_PROFILE, check_in_profile, D_UNIT, check_unit, D1, D2

import pyroll.core as pr


def test_in_profile():
    p = from_dict(D_IN_PROFILE, {})
    check_in_profile(p)


def test_unit():
    u = from_dict(D_UNIT, {})
    check_unit(u)


def test_input1():
    p, u = dict_input(D1)
    check_in_profile(p)
    check_unit(u)


def test_input2():
    p, u = dict_input(D2)
    check_in_profile(p)

    assert isinstance(u, pr.PassSequence)
    check_unit(u[0])
