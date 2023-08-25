from collections.abc import Collection, Mapping
from dataclasses import is_dataclass
from typing import Callable, Any, get_args, get_origin

from pyroll.from_dict import Config
from schema import And, Or, Schema, Optional, Regex
from inspect import signature, Parameter
import pyroll.core as pr


def create_input_schema():
    """
    Create a validation schema for a complete PyRolL input via dict, JSON, yaml or similar.

    :return: a ``schema.Schema`` instance
    """
    profile_schema = Or(
        create_schema(pr.Profile, pr.Profile.round),
        create_schema(pr.Profile, pr.Profile.diamond),
        create_schema(pr.Profile, pr.Profile.square),
        create_schema(pr.Profile, pr.Profile.box),
        create_schema(pr.Profile, pr.Profile.from_groove),
        create_schema(pr.Profile, pr.Profile.from_polygon),
        create_schema(pr.RoundProfile),
        create_schema(pr.DiamondProfile),
        create_schema(pr.SquareProfile),
        create_schema(pr.BoxProfile),
    )
    roll_pass_schema = create_schema(pr.RollPass)
    transport_schema = create_schema(pr.Transport)
    rotator_schema = create_schema(pr.Rotator)
    sequence_schema = create_schema(pr.PassSequence)
    units_schemas = roll_pass_schema, transport_schema, rotator_schema, sequence_schema

    schema = Schema(
        {
            Config.NAMESPACES_KEY: {str: str},
            Config.IN_PROFILE_KEY: profile_schema,
            Or(Config.UNIT_KEY, Config.SEQUENCE_KEY): Or(
                [*units_schemas],
                *units_schemas
            )
        }
    )

    return schema


def create_schema(type: type, ctor: Callable = None):
    """
    Create a validation schema for a given type and constructor.

    :param type: the type to instantiate
    :param ctor: the constructor/factory method to use (equals ``t`` if omitted)
    :return: a ``schema.Schema`` instance
    """
    if ctor is None:
        ctor = type

    return Schema(_create_schema_for_pyroll(type, ctor))


def _analyse_ctor_arg(info: Parameter):
    name = info.name
    annotation = info.annotation

    if str(annotation).startswith("typing.Optional"):
        data_type = get_args(annotation)[0]
        required = False
    elif info.default is not Parameter.empty:
        data_type = annotation
        required = False
    else:
        data_type = annotation
        required = True
    return name, data_type, required


def _create_schema_from_constructor(ctor):
    ctor_sig = signature(ctor)
    args = [
        _analyse_ctor_arg(info)
        for arg, info in ctor_sig.parameters.items() if arg not in {"kwargs", "parent"}
    ]
    args_schema = dict(
        _create_schema_for_arg(*arg)
        for arg in args
    )

    return {Optional(Config.FACTORY_KEY): Regex(rf"[\w.]*{ctor.__qualname__}")} | args_schema


def _create_schema_for_pyroll(t, ctor):
    ctor_schema = _create_schema_from_constructor(ctor)

    hook_args = [
        (name, hook.type)
        for name, hook in t.__dict__.items() if isinstance(hook, pr.Hook)
    ]

    hook_schema = dict(
        _create_schema_for_arg(arg[0], arg[1], False)
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


def _create_schema_for_arg(name, type, required):
    type_schema = _create_schema_for_type(type)

    if not required:
        return Optional(name), type_schema
    return name, type_schema
