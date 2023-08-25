from dataclasses import dataclass

import pytest

from pyroll.from_dict import Config
from pyroll.from_dict.from_dict import from_dict, dict_input
from tests.conf import D_IN_PROFILE, check_in_profile, D_UNIT, check_unit, D1, D2

import pyroll.core as pr


def test_in_profile():
    p = from_dict(D_IN_PROFILE, {})
    check_in_profile(p)


@pytest.mark.parametrize(
    ("d", "cls"),
    [
        ({"diameter": 1}, "round"),
        ({"radius": 1}, "round"),
        ({"side": 1}, "square"),
        ({"diagonal": 1}, "square"),
    ]
)
def test_in_profile_heuristic(d, cls):
    p = from_dict(d, {})
    assert cls in p.classifiers


@pytest.mark.parametrize(
    "d",
    [
        {"height": 1, "width": 1},
    ]
)
def test_in_profile_heuristic_error(d):
    with pytest.raises(ValueError):
        from_dict(d, {})


def test_unit():
    u = from_dict(D_UNIT, {})
    check_unit(u)


@pytest.mark.parametrize(
    ("d", "cls"),
    [
        ({"roll": {"groove": None}}, pr.RollPass),
        ({"duration": 1}, pr.Transport),
        ({"rotation": 1}, pr.Rotator),
        ({"units": []}, pr.PassSequence),
    ]
)
def test_unit_heuristic(d, cls):
    u = from_dict(d, {})
    assert isinstance(u, cls)


def test_input1():
    p, u = dict_input(D1)
    check_in_profile(p)
    check_unit(u)


def test_input2():
    p, u = dict_input(D2)
    check_in_profile(p)

    assert isinstance(u, pr.PassSequence)
    check_unit(u[0])


def test_dataclass_heuristic():
    @dataclass
    class DataSet:
        a: int

    class Host(pr.HookHost):
        def __init__(self, hook1):
            super().__init__()
            self.hook1 = hook1

        hook1 = pr.Hook[DataSet]()

    inst = from_dict(dict(
        __ctor__=Host,
        hook1=dict(a=42)
    ), {})

    assert isinstance(inst.hook1, DataSet)
    assert inst.hook1.a == 42
