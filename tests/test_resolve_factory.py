from pyroll.input_text.resolve_factory import resolve_factory
import pyroll.core as pr


def test_alias_class():
    assert resolve_factory("pr.RollPass", {"pr": "pyroll.core"}) is pr.RollPass


def test_sys_class():
    assert resolve_factory("pyroll.core.RollPass") is pr.RollPass


def test_alias_factory():
    # instances are always created anew, so 'is' does not work
    assert repr(resolve_factory("pr.Profile.round", {"pr": "pyroll.core"})) == repr(pr.Profile.round)


def test_sys_factory():
    # instances are always created anew, so 'is' does not work
    assert repr(resolve_factory("pyroll.core.Profile.round")) == repr(pr.Profile.round)
