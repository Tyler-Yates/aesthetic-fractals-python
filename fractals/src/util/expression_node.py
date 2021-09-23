from typing import Optional, Union

UNARY_OPERATORS = frozenset(["sin", "cos", "abs"])
BINARY_OPERATORS = frozenset(["+", "-", "*", "/"])
VARIABLES = frozenset(["x", "y"])

VALID_NODE_VALUES = frozenset.union(UNARY_OPERATORS, BINARY_OPERATORS, VARIABLES)


class ExpressionNode:
    def __init__(
        self,
        value: Union[str, float],
        left: Optional["ExpressionNode"] = None,
        right: Optional["ExpressionNode"] = None,
    ):
        # Simplify by always using lower-case
        if isinstance(value, str):
            value = value.lower()

        if value in VALID_NODE_VALUES:
            # String variable or operator
            self.value = value
        else:
            # Constant float values are also acceptable
            try:
                self.value = float(value)
            except ValueError:
                raise ValueError(f"Value {value} is not allowed. Allowed values are: {VALID_NODE_VALUES} or a number")

        # Default to no parent node
        self.parent: Optional[ExpressionNode] = None

        # Set left and right (if present) and also make this node the parent of the children
        self.left = left
        if left is None:
            if self.is_binary_operator() or self.is_unary_operator():
                raise ValueError("Operator nodes must pass children in to constructor")
        else:
            left.parent = self

        self.right = right
        if right is None:
            if self.is_binary_operator():
                raise ValueError("Operator nodes must pass children in to constructor")
        else:
            right.parent = self

    def is_operator(self):
        return (self.value in BINARY_OPERATORS) or (self.value in UNARY_OPERATORS)

    def is_binary_operator(self):
        return self.value in BINARY_OPERATORS

    def is_unary_operator(self):
        return self.value in UNARY_OPERATORS

    def is_leaf(self):
        return (self.left is None) and (self.right is None)

    def is_variable(self):
        return self.value in VARIABLES
