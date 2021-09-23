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
        ExpressionNode("sin", left=ExpressionNode(9))

    def test_expression_unary_invalid(self):
        # Unary operator nodes need to pass in the left node
        with pytest.raises(ValueError):
            ExpressionNode("sin")

    def test_expression_binary(self):
        ExpressionNode("*", left=ExpressionNode(9), right=ExpressionNode("x"))

    def test_expression_binary_invalid(self):
        # Unary operator nodes need to pass in both the left and right nodes
        with pytest.raises(ValueError):
            ExpressionNode("*")
        with pytest.raises(ValueError):
            ExpressionNode("*", left=ExpressionNode(9))

    def test_node_relationships(self):
        left_node = ExpressionNode(9)
        right_node = ExpressionNode("x")
        parent_node = ExpressionNode("*", left=left_node, right=right_node)

        assert left_node.parent == parent_node
        assert right_node.parent == parent_node
        assert parent_node.left == left_node
        assert parent_node.right == right_node
