from collections.abc import Sequence, Collection, Mapping
from dataclasses import dataclass
from typing import Callable, Any, get_args, get_origin, Union

from schema import And, Or, Schema, Optional
from inspect import signature, Parameter
import pyroll.core as pr


class _PrimaryArg:
    def __init__(self, name: str, annotation):
        self.name: str = name
        self.annotation: Any = annotation

        if str(annotation).startswith("typing.Optional"):
            self.data_type = get_args(annotation)[0]
            self.required = False
        else:
            self.data_type = annotation
            self.required = True


def create_schema(t: type, ctor: Callable = None):
    if ctor is None:
        ctor = t

    ctor_sig = signature(ctor)
    primary_args = [
        _PrimaryArg(arg, info.annotation)
        for arg, info in ctor_sig.parameters.items() if arg not in {"kwargs", "parent"}
    ]

    secondary_args = [
        (name, hook.type)
        for name, hook in t.__dict__.items() if isinstance(hook, pr.Hook)
    ]

    primary_schema = dict(
        _create_schema_for_arg(arg.name, arg.data_type, not arg.required)
        for arg in primary_args
    )

    secondary_schema = dict(
        _create_schema_for_arg(arg[0], arg[1], True)
        for arg in secondary_args
    )

    return Schema(
        primary_schema | secondary_schema
    )


def _create_schema_for_type(type):
    try:
        origin = get_origin(type)

        if origin is not None:
            args = get_args(type)

            if str(origin).startswith("typing.Union"):
                return And(*[_create_schema_for_type(arg) for arg in args])

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

        raise TypeError
    except TypeError:
        return {str: str}


def _create_schema_for_arg(name, type, optional):
    type_schema = _create_schema_for_type(type)

    if optional:
        return Optional(name), type_schema
    return name, type_schema
