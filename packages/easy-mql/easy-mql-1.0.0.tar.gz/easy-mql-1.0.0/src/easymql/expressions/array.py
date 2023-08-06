from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.core import Suppress
from easymql.identifiers import *
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class ArrayElemAt(Grammar, ExpressionAction):

    grammar = (
        ARRAY_ELEM_AT + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN
    )


class ArrayToObject(Grammar, ExpressionAction):

    grammar = ARRAY_TO_OBJECT + LPAREN + expression_proxy + RPAREN


class ConcatArrays(Grammar, ExpressionAction):

    grammar = (
        CONCAT_ARRAYS
        + LPAREN
        + DelimitedList(expression_proxy, min=2, max=...)
        + RPAREN
    )


class Filter(Grammar, ExpressionAction):
    grammar = (
        Suppress(FILTER)
        + LPAREN
        + DelimitedList(expression_proxy, min=3, max=3)
        + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {"$filter": {"input": tokens[0], "as": tokens[1], "cond": tokens[2]}}


class First(Grammar, ExpressionAction):

    grammar = FIRST + LPAREN + expression_proxy + RPAREN


class In(Grammar, ExpressionAction):

    grammar = IN + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN


class IndexOfArray(Grammar, ExpressionAction):

    grammar = (
        INDEX_OF_ARRAY + LPAREN + DelimitedList(expression_proxy, min=2, max=4) + RPAREN
    )


class IsArray(Grammar, ExpressionAction):

    grammar = IS_ARRAY + LPAREN + expression_proxy + RPAREN


class Last(Grammar, ExpressionAction):

    grammar = LAST + LPAREN + expression_proxy + RPAREN


class Map(Grammar, ExpressionAction):
    grammar = (
        Suppress(MAP) + LPAREN + DelimitedList(expression_proxy, min=3, max=3) + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {"$map": {"input": tokens[0], "as": tokens[1], "in": tokens[2]}}


class ObjectToArray(Grammar, ExpressionAction):

    grammar = Suppress(OBJECT_TO_ARRAY) + LPAREN + expression_proxy + RPAREN

    @staticmethod
    def action(tokens):
        return {"$objectToArray": tokens[0]}


class Range(Grammar, ExpressionAction):

    grammar = RANGE + LPAREN + DelimitedList(expression_proxy, min=2, max=3) + RPAREN


class Reduce(Grammar, ExpressionAction):
    grammar = (
        Suppress(REDUCE)
        + LPAREN
        + DelimitedList(expression_proxy, min=3, max=3)
        + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {
            "$reduce": {"input": tokens[0], "initialValue": tokens[1], "in": tokens[2]}
        }


class ReverseArray(Grammar, ExpressionAction):

    grammar = REVERSE_ARRAY + LPAREN + expression_proxy + RPAREN


class Size(Grammar, ExpressionAction):

    grammar = SIZE + LPAREN + expression_proxy + RPAREN


class Slice(Grammar, ExpressionAction):

    grammar = SLICE + LPAREN + DelimitedList(expression_proxy, min=2, max=3) + RPAREN


class Zip(Grammar, ExpressionAction):
    grammar = (
        Suppress(ZIP) + LPAREN + DelimitedList(expression_proxy, min=1, max=3) + RPAREN
    )

    @staticmethod
    def action(tokens):

        result = {"inputs": tokens[0]}
        if len(tokens) >= 2:
            result["useLongestLength"] = tokens[1]

        if len(tokens) == 3:
            result["defaults"] = tokens[2]

        return {"$zip": result}


ArrayExpression = (
    ArrayElemAt
    | ArrayToObject
    | ConcatArrays
    | Filter
    | First
    | In
    | IndexOfArray
    | IsArray
    | Last
    | Map
    | ObjectToArray
    | Range
    | Reduce
    | ReverseArray
    | Size
    | Slice
    | Zip
)
