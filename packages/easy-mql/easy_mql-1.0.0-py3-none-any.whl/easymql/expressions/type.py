from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.identifiers import *
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class Convert(Grammar):

    grammar = CONVERT + LPAREN + DelimitedList(expression_proxy, min=2, max=4) + RPAREN

    @classmethod
    def action(cls, tokens):
        return {'$convert': dict(zip(('input', 'to', 'onError', 'onNull'), tokens[1:]))}


class IsNumber(Grammar, ExpressionAction):

    grammar = IS_NUMBER + LPAREN + expression_proxy + RPAREN


class ToBool(Grammar, ExpressionAction):

    grammar = TO_BOOL + LPAREN + expression_proxy + RPAREN


class ToDate(Grammar, ExpressionAction):

    grammar = TO_DATE + LPAREN + expression_proxy + RPAREN


class ToDecimal(Grammar, ExpressionAction):

    grammar = TO_DECIMAL + LPAREN + expression_proxy + RPAREN


class ToDouble(Grammar, ExpressionAction):

    grammar = TO_DOUBLE + LPAREN + expression_proxy + RPAREN


class ToInt(Grammar, ExpressionAction):

    grammar = TO_INT + LPAREN + expression_proxy + RPAREN


class ToLong(Grammar, ExpressionAction):

    grammar = TO_LONG + LPAREN + expression_proxy + RPAREN


class ToObjectId(Grammar, ExpressionAction):

    grammar = TO_OBJECT_ID + LPAREN + expression_proxy + RPAREN


class ToString(Grammar, ExpressionAction):

    grammar = TO_STRING + LPAREN + expression_proxy + RPAREN


class Type(Grammar, ExpressionAction):

    grammar = TYPE + LPAREN + expression_proxy + RPAREN


TypeExpression = (
    Convert
    | IsNumber
    | ToBool
    | ToDate
    | ToDecimal
    | ToDouble
    | ToInt
    | ToLong
    | ToObjectId
    | ToString
    | Type
)
