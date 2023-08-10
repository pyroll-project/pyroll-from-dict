import pyroll.core as pr
from pyroll.input_text import Config

D_IN_PROFILE = {
    Config.FACTORY_KEY: 'Profile.round',
    'diameter': 0.01,
    'strain': 0,
    'temperature': 1273.15
}

D_UNIT = {
    Config.FACTORY_KEY: 'RollPass',
    'gap': 0.001,
    'roll': {
        Config.FACTORY_KEY: 'Roll',
        'nominal_radius': 0.1,
        'rotational_frequency': 1,
        'groove': {
            Config.FACTORY_KEY: 'CircularOvalGroove',
            'r1': 0.002,
            'r2': 0.02,
            'depth': 0.002
        }
    }
}

D_NAMESPACES = {
    "pr": "pyroll.core"
}

D1 = {
    Config.NAMESPACES_KEY: D_NAMESPACES,
    Config.IN_PROFILE_KEY: D_IN_PROFILE,
    Config.UNIT_KEY: D_UNIT,
}

D2 = {
    Config.NAMESPACES_KEY: D_NAMESPACES,
    Config.IN_PROFILE_KEY: D_IN_PROFILE,
    Config.UNIT_KEY: [D_UNIT],
}


def check_in_profile(p: pr.Profile):
    assert "round" in p.classifiers
    assert p.height == 0.01
    assert p.strain == 0
    assert p.temperature == 1273.15


def check_unit(u: pr.Unit):
    assert isinstance(u, pr.RollPass)
    assert u.gap == 1e-3
    assert "oval" in u.classifiers
