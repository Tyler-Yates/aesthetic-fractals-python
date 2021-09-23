import random

from fractals.src.util.expression_node import ExpressionNode


class Expression:
    def __init__(self, root_node: ExpressionNode):
        self.root = root_node

    @staticmethod
    def _evaluate(current_node: ExpressionNode, x: float, y: float) -> float:
        if current_node is None:
            return -1.0

    def evaluate(self, x: float, y: float) -> float:
        return self._evaluate(self.root, x, y)

    @staticmethod
    def _generate_random_x_equation() -> "Expression":
        # Random constants
        a = random.uniform(-3.0, 3.0)
        b = random.uniform(-3.0, 3.0)

        # Left half of addition
        a_1 = ExpressionNode(a)
        y_1 = ExpressionNode("y")
        mul_1 = ExpressionNode("*", left=a_1, right=y_1)
        sin_1 = ExpressionNode("sin", left=mul_1)

        # Right half of addition
        a_2 = ExpressionNode(a)
        x_1 = ExpressionNode("x")
        mul_2 = ExpressionNode("*", left=a_2, right=x_1)
        cos_1 = ExpressionNode("cos", left=mul_2)
        b_1 = ExpressionNode(b)
        mul_3 = ExpressionNode("*", b_1, cos_1)

        # Root
        root = ExpressionNode("+", sin_1, mul_3)
        return Expression(root)
