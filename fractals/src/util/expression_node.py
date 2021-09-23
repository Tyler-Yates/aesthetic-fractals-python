from typing import Optional, Union

UNARY_OPERATORS = frozenset(["sin", "cos", "abs"])
BINARY_OPERATORS = frozenset(["+", "-", "*", "/"])
VARIABLES = frozenset(["x", "y"])

VALID_NODE_VALUES = frozenset.union(UNARY_OPERATORS, BINARY_OPERATORS, VARIABLES)


class ExpressionNode:
    def __init__(self, value: Union[str, float], left: Optional['ExpressionNode'] = None,
                 right: Optional['ExpressionNode'] = None):
        # Simplify by always using lower-case
        value = value.lower()

        # Make sure the value is valid
        if value not in VALID_NODE_VALUES:
            # Constant values are also acceptable
            try:
                float(value)
            except ValueError:
                raise ValueError(f"Value {value} is not allowed. Allowed values are: {VALID_NODE_VALUES} or a number")

        self.value = value

        self.parent: Optional[ExpressionNode] = None
        self.left = left
        self.right = right

    def is_operator(self):
        return (self.value in BINARY_OPERATORS) or (self.value in UNARY_OPERATORS)

    def is_binary_operator(self):
        return self.value in BINARY_OPERATORS

    def is_unary_operator(self):
        return self.value in UNARY_OPERATORS

    def is_leaf(self):
        return (self.left is None) and (self.right is None)
