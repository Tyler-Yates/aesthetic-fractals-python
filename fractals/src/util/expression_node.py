from typing import Optional

UNARY_OPERATORS = frozenset(["sin", "cos", "abs"])
BINARY_OPERATORS = frozenset(["+", "-", "*", "/"])
VARIABLES = frozenset(["x", "y"])

VALID_NODE_VALUES = frozenset.union(UNARY_OPERATORS, BINARY_OPERATORS, VARIABLES)


class ExpressionNode:
    def __init__(self, value: str):
        value = value.lower()
        if value not in VALID_NODE_VALUES:
            raise ValueError(f"Value {value} is not allowed. Allowed values are: {VALID_NODE_VALUES}")

        self.value = value

        self.parent: Optional[ExpressionNode] = None
        self.left: Optional[ExpressionNode] = None
        self.right: Optional[ExpressionNode] = None

    def is_operator(self):
        return (self.value in BINARY_OPERATORS) or (self.value in UNARY_OPERATORS)

    def is_binary_operator(self):
        return self.value in BINARY_OPERATORS

    def is_unary_operator(self):
        return self.value in UNARY_OPERATORS

    def is_leaf(self):
        return (self.left is None) and (self.right is None)
