from pyroll.from_dict.resolve import resolve
import pyroll.core as pr


def test_alias_class():
    assert resolve("pr.RollPass", {"pr": pr}) is pr.RollPass


def test_core_class():
    assert resolve("RollPass") is pr.RollPass


def test_alias_factory():
    # instances are always created anew, so 'is' does not work
    assert repr(resolve("pr.Profile.round", {"pr": pr})) == repr(pr.Profile.round)


def test_core_factory():
    # instances are always created anew, so 'is' does not work
    assert repr(resolve("Profile.round")) == repr(pr.Profile.round)
