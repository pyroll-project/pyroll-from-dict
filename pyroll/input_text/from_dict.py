from typing import Callable

import pyroll.core as pr

from .config import Config
from .resolve import resolve


def from_dict(d: dict, namespaces: dict[str, ...]) -> ...:
    factory = resolve(d[Config.FACTORY_KEY], namespaces)
    args = d.copy()
    del args[Config.FACTORY_KEY]

    for k, v in args.items():
        if isinstance(v, dict):
            args[k] = from_dict(v, namespaces)

    return factory(**args)


def register_hook_function(d: dict[str, ...]) -> pr.HookFunction:
    try:
        tryfirst = bool(d["tryfirst"])
    except KeyError:
        tryfirst = False

    try:
        trylast = bool(d["trylast"])
    except KeyError:
        trylast = False

    try:
        wrapper = bool(d["wrapper"])
    except KeyError:
        wrapper = False

    hook: pr.Hook = resolve(d["hook"])
    code = compile(d["code"], "<string>", "eval")

    def func(self, cycle):
        return eval(code, {}, {"self": self, "cycle": cycle})

    return hook.add_function(func, tryfirst, trylast, wrapper)
