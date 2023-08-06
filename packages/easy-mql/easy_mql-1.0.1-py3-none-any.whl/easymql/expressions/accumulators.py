from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.identifiers import *
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class Avg(Grammar, ExpressionAction):

    grammar = AVG + LPAREN + DelimitedList(expression_proxy, min=1, max=...) + RPAREN


class Max(Grammar, ExpressionAction):

    grammar = MAX + LPAREN + DelimitedList(expression_proxy, min=1, max=...) + RPAREN


class Min(Grammar, ExpressionAction):

    grammar = MIN + LPAREN + DelimitedList(expression_proxy, min=1, max=...) + RPAREN


class StdDevPop(Grammar, ExpressionAction):

    grammar = (
        STD_DEV_POP + LPAREN + DelimitedList(expression_proxy, min=1, max=...) + RPAREN
    )


class StdDevSamp(Grammar, ExpressionAction):

    grammar = (
        STD_DEV_SAMP + LPAREN + DelimitedList(expression_proxy, min=1, max=...) + RPAREN
    )


class Sum(Grammar, ExpressionAction):

    grammar = SUM + LPAREN + DelimitedList(expression_proxy, min=1, max=...) + RPAREN


AccumulatorExpression = Avg | Max | Min | StdDevPop | StdDevSamp | Sum
