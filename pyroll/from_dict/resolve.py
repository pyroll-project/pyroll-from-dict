import sys
import importlib

import pyroll.core as pr


def resolve(name: str, namespaces: dict[str, ...] = None) -> type:
    if namespaces is None:
        namespaces = {}
    namespace = None
    object_name = None

    for key in namespaces.keys():
        if name.startswith(key):
            namespace = namespaces[key]
            object_name = name[len(key) + 1:]
            break

    if not namespace:
        namespace = pr
        object_name = name

    for attr in object_name.split("."):
        namespace = getattr(namespace, attr)

    return namespace
