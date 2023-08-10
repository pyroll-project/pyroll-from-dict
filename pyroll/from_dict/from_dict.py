import importlib

import pyroll.core as pr

from .config import Config
from .explicit_functions import is_function, parse_function
from .resolve import resolve


def dict_input(d: dict) -> tuple[pr.Profile, pr.Unit]:
    namespaces = {k: importlib.import_module(v) for k, v in d[Config.NAMESPACES_KEY].items()}

    in_profile = from_dict(d[Config.IN_PROFILE_KEY], namespaces)

    d_unit = d[Config.UNIT_KEY]
    if isinstance(d_unit, list):
        unit = pr.PassSequence([from_dict(u, namespaces) for u in d_unit])
    else:
        unit = from_dict(d_unit, namespaces)

    return in_profile, unit


def from_dict(d: dict, namespaces: dict[str, ...]) -> ...:
    factory = resolve(d[Config.FACTORY_KEY], namespaces)
    args = d.copy()
    del args[Config.FACTORY_KEY]

    for k, v in args.items():
        if isinstance(v, dict):
            args[k] = from_dict(v, namespaces)
        if is_function(v):
            args[k] = parse_function(v, namespaces)

    return factory(**args)
