# PyRoll From Dict Extension

This extension is meant to create PyRolL objects from plain `dict` structures.

## Import PyRolL Objects

For example to create a `RollPass` instance with the related `Roll` and `Groove` objects use the following:

```python
from pyroll.from_dict import from_dict

roll_pass = from_dict({
    '__ctor__': 'RollPass',
    'gap': 0.001,
    'roll': {
        '__ctor__': 'Roll',
        'nominal_radius': 0.1,
        'rotational_frequency': 1,
        'groove': {
            '__ctor__': 'CircularOvalGroove',
            'r1': 0.002,
            'r2': 0.02,
            'depth': 0.002
        }
    }
}, {})
```

The class resp. factory function can be given with the `__ctor__` key.
By default, class and object names therein are resolved in the `pyroll.core` namespace.
The key can be changed with the `pyroll.from_dict.Config.FACTORY_KEY` config parameter.
The second argument to `from_dict` is a dict of namespaces to use additionally for resolving constructor names.
The key must be than used as prefix to the object name in dot notation like in the following example (although you may
resolve `RollPass` without prefix, because it is in the `pyroll.core` namespace).

```python
from pyroll.from_dict import from_dict

roll_pass = from_dict({
    '__ctor__': 'pr.RollPass',
    ...
}, {"pr": "pyroll.core"})
```

## Import Whole Input Sets

The second main function of this package is `dict_input`.
It reads from a larger dict structure containing an incoming profile, a pass sequence and namespace definitions.
It returns a tuple of in profile and pass sequence.

```python
from pyroll.from_dict import dict_input

in_profile, sequence = dict_input({
    'namespaces': {'pr': 'pyroll.core', 'np': 'numpy'},
    'in_profile': {
        '__ctor__': 'Profile.round',
        'diameter': 0.01,
        'strain': 0,
        'temperature': 1273.15,
        'density': 'func: 7.85 / (1 + 3 * 3.5e-3 * (self.temperature - 273.15))'
    },
    'unit': [
        {
            '__ctor__': 'RollPass',
            'gap': 0.001,
            'roll': {
                '__ctor__': 'Roll',
                'nominal_radius': 0.1,
                'rotational_frequency': 1,
                'groove': {
                    '__ctor__': 'CircularOvalGroove',
                    'r1': 0.002,
                    'r2': 0.02,
                    'depth': 0.002
                }
            }
        }
    ]
})
```

The namespaces are used in resolving all specified objects.
The keys for namespaces, in profile and unit/sequence can be configured
with `pyroll.from_dict.Config.NAMESPACES_KEY`, `pyroll.from_dict.Config.IN_PROFILE_KEY`
and `pyroll.from_dict.Config.UNIT_KEY`.
The value of the unit can be a single unit definition or a list.
The list will be automatically converted into an instance of `PassSequence`.

As you can see in the `density` field of the in profile, you may give explicit hook functions by providing a string of
the structure `"func: <some expression>` similar to a lambda function.
Whitespace in this string is ignored.
The only argument to this function is `self`, the reference to the respective instance.
The function expression will be compiled and executed using `eval()`.
You may use all modules defined in the namespaces from within the function (so for example you may use `np` for `numpy`
here.