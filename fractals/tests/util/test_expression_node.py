import pytest

from fractals.src.util.expression_node import ExpressionNode


class TestExpressionNode:
    def test_expression_value(self):
        expression_node = ExpressionNode("x")
        assert "x" == expression_node.value

    def test_expression_valid_leaf_values(self):
        ExpressionNode("x")
        ExpressionNode("0")
        ExpressionNode("9")
        ExpressionNode("9.9")
        ExpressionNode("-9.9")
        ExpressionNode(0)
        ExpressionNode(9)
        ExpressionNode(9.9)
        ExpressionNode(-9.9)

    def test_expression_invalid_value(self):
        with pytest.raises(ValueError):
            ExpressionNode("asgasga")

    def test_expression_unary(self):
        ExpressionNode(9)
