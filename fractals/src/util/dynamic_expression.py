import math

from fractals.src.util.expression import Expression
from fractals.src.util.expression_node import ExpressionNode


class DynamicExpression(Expression):
    def __init__(self, root_node: ExpressionNode):
        self.root = root_node

    def _evaluate(self, current_node: ExpressionNode, x: float, y: float) -> float:
        if current_node is None:
            return -1.0

        if current_node.is_leaf():
            if current_node.is_variable():
                if current_node.value == "x":
                    return x
                elif current_node.value == "y":
                    return y
                else:
                    raise ValueError(f"Unknown variable {current_node.value}")
            else:
                return float(current_node.value)

        if current_node.value == "+":
            return self._evaluate(current_node.left, x, y) + self._evaluate(current_node.right, x, y)
        if current_node.value == "-":
            return self._evaluate(current_node.left, x, y) - self._evaluate(current_node.right, x, y)
        if current_node.value == "*":
            return self._evaluate(current_node.left, x, y) * self._evaluate(current_node.right, x, y)
        if current_node.value == "/":
            return self._evaluate(current_node.left, x, y) / self._evaluate(current_node.right, x, y)
        if current_node.value == "sin":
            return math.sin(self._evaluate(current_node.left, x, y))
        if current_node.value == "cos":
            return math.cos(self._evaluate(current_node.left, x, y))
        if current_node.value == "abs":
            return abs(self._evaluate(current_node.left, x, y))

        raise ValueError(f"Unknown node value {current_node.value}")

    def evaluate(self, x: float, y: float) -> float:
        return self._evaluate(self.root, x, y)
