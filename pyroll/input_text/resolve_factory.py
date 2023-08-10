import sys
import importlib


def resolve_factory(name: str, imports: dict[str, str] = None) -> type:
    if imports is None:
        imports = dict()
    module_name = None
    object_name = None

    for key in imports.keys():
        if name.startswith(key):
            module_name = imports[key]
            object_name = name[len(key) + 1:]
            break

    if not module_name:
        keys = sorted(sys.modules.keys(), key=len, reverse=True)

        for key in keys:
            if name.startswith(key):
                module_name = key
                object_name = name[len(key) + 1:]
                break

    if not module_name or not object_name:
        raise ValueError()

    obj = importlib.import_module(module_name)

    for attr in object_name.split("."):
        obj = getattr(obj, attr)

    return obj
