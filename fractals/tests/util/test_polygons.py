import pytest

from fractals.src.util.expression_node import ExpressionNode


class TestExpressionNode:
    def test_expression_value(self):
        expression_node = ExpressionNode("x")
        assert "x" == expression_node.value

    def test_expression_invalid_value(self):
        with pytest.raises(ValueError):
            ExpressionNode("asgasga")
