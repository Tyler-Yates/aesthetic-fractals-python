from fractals.src.util.dynamic_expression import DynamicExpression
from fractals.src.util.expression_node import ExpressionNode


class TestExpression:
    def test_simple_expression(self):
        left_node = ExpressionNode(9)
        right_node = ExpressionNode("x")
        root_node = ExpressionNode("*", left=left_node, right=right_node)
        expression = DynamicExpression(root_node)

        assert 9.0 == expression.evaluate(x=1.0, y=1.0)
        assert 18.0 == expression.evaluate(x=2.0, y=1.0)
