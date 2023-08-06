from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.identifiers import *
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class Sin(Grammar, ExpressionAction):

    grammar = SIN + LPAREN + expression_proxy + RPAREN


class Cos(Grammar, ExpressionAction):

    grammar = COS + LPAREN + expression_proxy + RPAREN


class Tan(Grammar, ExpressionAction):

    grammar = TAN + LPAREN + expression_proxy + RPAREN


class Asin(Grammar, ExpressionAction):

    grammar = ASIN + LPAREN + expression_proxy + RPAREN


class Acos(Grammar, ExpressionAction):

    grammar = ACOS + LPAREN + expression_proxy + RPAREN


class Atan(Grammar, ExpressionAction):

    grammar = ATAN + LPAREN + expression_proxy + RPAREN


class Atan2(Grammar, ExpressionAction):

    grammar = ATAN2 + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN


class Asinh(Grammar, ExpressionAction):

    grammar = ASINH + LPAREN + expression_proxy + RPAREN


class Acosh(Grammar, ExpressionAction):

    grammar = ACOSH + LPAREN + expression_proxy + RPAREN


class Atanh(Grammar, ExpressionAction):

    grammar = ATANH + LPAREN + expression_proxy + RPAREN


class DegreesToRadians(Grammar, ExpressionAction):

    grammar = DEGREES_TO_RADIANS + LPAREN + expression_proxy + RPAREN


class RadiansToDegrees(Grammar, ExpressionAction):

    grammar = RADIANS_TO_DEGREES + LPAREN + expression_proxy + RPAREN


TrigonometryExpression = (
    Sin
    | Cos
    | Tan
    | Asin
    | Acos
    | Atan
    | Atan2
    | Asinh
    | Acosh
    | Atanh
    | DegreesToRadians
    | RadiansToDegrees
)
