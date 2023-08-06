from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.datatypes.composite import Array
from easymql.identifiers import *
from easymql.meta import Grammar
from easymql.utils import DelimitedList
from easymql.proxies import expression_proxy


class All(Grammar, ExpressionAction):

    grammar = ALL + LPAREN + expression_proxy + RPAREN

    @staticmethod
    def action(tokens):
        return {'$allElementsTrue': [tokens[-1]]}


class Any(Grammar, ExpressionAction):

    grammar = ANY + LPAREN + expression_proxy + RPAREN

    @staticmethod
    def action(tokens):
        return {'$anyElementTrue': [tokens[-1]]}


class SetDifference(Grammar, ExpressionAction):

    grammar = (
        SET_DIFFERENCE + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN
    )


class SetEquals(Grammar, ExpressionAction):

    grammar = SET_EQUALS + LPAREN + DelimitedList(expression_proxy) + RPAREN


class SetIntersection(Grammar, ExpressionAction):

    grammar = SET_INTERSECTION + LPAREN + DelimitedList(expression_proxy) + RPAREN


class SetIsSubset(Grammar, ExpressionAction):

    grammar = (
        SET_IS_SUBSET + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN
    )


class SetUnion(Grammar, ExpressionAction):

    grammar = SET_UNION + LPAREN + DelimitedList(expression_proxy) + RPAREN


SetExpression = (
    All | Any | SetDifference | SetEquals | SetIntersection | SetIsSubset | SetUnion
)
