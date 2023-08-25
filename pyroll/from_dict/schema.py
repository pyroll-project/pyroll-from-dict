from collections.abc import Collection, Mapping
from dataclasses import is_dataclass
from typing import Callable, Any, get_args, get_origin

from pyroll.from_dict import Config
from schema import And, Or, Schema, Optional, Regex
from inspect import signature, Parameter
import pyroll.core as pr


class _PrimaryArg:
    def __init__(self, name: str, info: Parameter):
        annotation = info.annotation
        self.name: str = name
        self.annotation: Any = annotation

        if str(annotation).startswith("typing.Optional"):
            self.data_type = get_args(annotation)[0]
            self.required = False
        elif info.default is not Parameter.empty:
            self.data_type = annotation
            self.required = False
        else:
            self.data_type = annotation
            self.required = True


def create_schema(t: type, ctor: Callable = None):
    if ctor is None:
        ctor = t

    return Schema(_create_schema_for_pyroll(t, ctor))


def _create_schema_from_constructor(ctor):
    ctor_sig = signature(ctor)
    args = [
        _PrimaryArg(arg, info)
        for arg, info in ctor_sig.parameters.items() if arg not in {"kwargs", "parent"}
    ]
    args_schema = dict(
        _create_schema_for_arg(arg.name, arg.data_type, not arg.required)
        for arg in args
    )

    return {Config.FACTORY_KEY: Regex(rf"[\w.]*{ctor.__qualname__}")} | args_schema


def _create_schema_for_pyroll(t, ctor):
    ctor_schema = _create_schema_from_constructor(ctor)

    hook_args = [
        (name, hook.type)
        for name, hook in t.__dict__.items() if isinstance(hook, pr.Hook)
    ]

    hook_schema = dict(
        _create_schema_for_arg(arg[0], arg[1], True)
        for arg in hook_args
    )
    return ctor_schema | hook_schema


def _create_schema_for_type(type):
    try:
        origin = get_origin(type)

        if origin is not None:
            args = get_args(type)

            if str(origin).startswith("typing.Union"):
                return Or(*[_create_schema_for_type(arg) for arg in args])

            if issubclass(origin, Callable):
                return str

            if issubclass(origin, Mapping):
                return {_create_schema_for_type(args[0]): _create_schema_for_type(args[1])}

            if issubclass(origin, Collection):
                return [_create_schema_for_type(args[0])]

        if issubclass(type, bool):
            return bool

        if issubclass(type, float):
            return Or(float, int)

        if issubclass(type, int):
            return int

        if issubclass(type, str):
            return str

        if issubclass(type, Mapping):
            return dict

        if issubclass(type, Collection):
            return list

        if issubclass(type, pr.HookHost):
            return _create_schema_for_pyroll(type, type)

        if issubclass(type, pr.GrooveBase):
            return Or(
                *
                [
                    _create_schema_from_constructor(g)
                    for n, g in pr.__dict__.items() if "Groove" in n and "Base" not in n
                ]
                + [{Config.FACTORY_KEY: str, str: str}]
            )

        if is_dataclass(type):
            return _create_schema_from_constructor(type)

        raise TypeError
    except TypeError:
        return {str: str}


def _create_schema_for_arg(name, type, optional):
    type_schema = _create_schema_for_type(type)

    if optional:
        return Optional(name), type_schema
    return name, type_schema
