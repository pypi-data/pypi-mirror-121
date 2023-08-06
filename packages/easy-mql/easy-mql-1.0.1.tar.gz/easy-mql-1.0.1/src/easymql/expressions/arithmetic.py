from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.identifiers import *
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class Abs(Grammar, ExpressionAction):

    grammar = ABS + LPAREN + expression_proxy + RPAREN


class Add(Grammar, ExpressionAction):

    grammar = ADD + LPAREN + DelimitedList(expression_proxy) + RPAREN


class Ceil(Grammar, ExpressionAction):

    grammar = CEIL + LPAREN + expression_proxy + RPAREN


class Divide(Grammar, ExpressionAction):

    grammar = DIVIDE + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN


class Exp(Grammar, ExpressionAction):

    grammar = EXP + LPAREN + expression_proxy + RPAREN


class Floor(Grammar, ExpressionAction):

    grammar = FLOOR + LPAREN + expression_proxy + RPAREN


class Ln(Grammar, ExpressionAction):

    grammar = LN + LPAREN + expression_proxy + RPAREN


class Log(Grammar, ExpressionAction):

    grammar = LOG + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN


class Log10(Grammar, ExpressionAction):

    grammar = LOG10 + LPAREN + expression_proxy + RPAREN


class Mod(Grammar, ExpressionAction):

    grammar = MOD + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN


class Multiply(Grammar, ExpressionAction):

    grammar = MULTIPLY + LPAREN + DelimitedList(expression_proxy) + RPAREN


class Pow(Grammar, ExpressionAction):

    grammar = POW + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN


class Round(Grammar, ExpressionAction):

    grammar = ROUND + LPAREN + DelimitedList(expression_proxy, min=1, max=2) + RPAREN


class Sqrt(Grammar, ExpressionAction):

    grammar = SQRT + LPAREN + expression_proxy + RPAREN


class Subtract(Grammar, ExpressionAction):

    grammar = SUBTRACT + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN


class Trunc(Grammar, ExpressionAction):

    grammar = TRUNC + LPAREN + DelimitedList(expression_proxy, min=1, max=2) + RPAREN


ArithmeticExpression = (
    Abs
    | Add
    | Ceil
    | Divide
    | Exp
    | Floor
    | Ln
    | Log
    | Log10
    | Mod
    | Multiply
    | Pow
    | Round
    | Sqrt
    | Subtract
    | Trunc
)
