from dataclasses import dataclass

import numpy as np

from pyroll.from_dict.explicit_functions import parse_function


@dataclass
class SelfDummy:
    radius: float


def test_parse_function():
    func = parse_function("func: np.sqrt(self.radius)", dict(np=np))

    assert func(SelfDummy(4)) == 2
