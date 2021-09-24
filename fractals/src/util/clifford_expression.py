from math import sin, cos
from typing import Tuple


def clifford_expression(x: float, y: float, a: float, b: float, c: float, d: float) -> Tuple[float, float]:
    return sin(a * y) + c * cos(a * x), sin(b * x) + d * cos(b * y)
