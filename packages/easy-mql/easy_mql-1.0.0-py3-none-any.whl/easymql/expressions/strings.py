from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN, COMMA
from easymql.core import Optional
from easymql.identifiers import *
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class Concat(Grammar, ExpressionAction):

    grammar = CONCAT + LPAREN + DelimitedList(expression_proxy, min=2) + RPAREN


class IndexOfBytes(Grammar, ExpressionAction):

    grammar = (
        INDEX_OF_BYTES + LPAREN + DelimitedList(expression_proxy, min=2, max=4) + RPAREN
    )


class IndexOfCP(Grammar, ExpressionAction):

    grammar = (
        INDEX_OF_CP + LPAREN + DelimitedList(expression_proxy, min=2, max=4) + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {'$indexOfCP': tokens[1:]}


class Trim(Grammar, ExpressionAction):

    grammar = TRIM + LPAREN + DelimitedList(expression_proxy, min=1, max=2) + RPAREN

    @staticmethod
    def action(tokens):
        return {'$trim': dict(zip(('input', 'chars'), tokens[1:]))}


class LTrim(Grammar, ExpressionAction):

    grammar = LTRIM + LPAREN + DelimitedList(expression_proxy, min=1, max=2) + RPAREN

    @staticmethod
    def action(tokens):
        return {'$ltrim': dict(zip(('input', 'chars'), tokens[1:]))}


class RTrim(Grammar, ExpressionAction):

    grammar = RTRIM + LPAREN + DelimitedList(expression_proxy, min=1, max=2) + RPAREN

    @staticmethod
    def action(tokens):
        return {'$rtrim': dict(zip(('input', 'chars'), tokens[1:]))}


class RegexFind(Grammar):

    grammar = (
        REGEX_FIND
        + LPAREN
        + expression_proxy
        + COMMA
        + expression_proxy
        + Optional(COMMA + expression_proxy)
        + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {'$regexFind': dict(zip(('input', 'regex', 'options'), tokens[1:]))}


class RegexFindAll(Grammar):

    grammar = (
        REGEX_FIND_ALL
        + LPAREN
        + expression_proxy
        + COMMA
        + expression_proxy
        + Optional(COMMA + expression_proxy)
        + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {'$regexFindAll': dict(zip(('input', 'regex', 'options'), tokens[1:]))}


class RegexMatch(Grammar):

    grammar = (
        REGEX_MATCH
        + LPAREN
        + expression_proxy
        + COMMA
        + expression_proxy
        + Optional(COMMA + expression_proxy)
        + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {'$regexMatch': dict(zip(('input', 'regex', 'options'), tokens[1:]))}


class Replace(Grammar):

    grammar = REPLACE + LPAREN + DelimitedList(expression_proxy, min=3, max=3) + RPAREN

    @staticmethod
    def action(tokens):
        return {'$replaceOne': dict(zip(('input', 'find', 'replacement'), tokens[1:]))}


class ReplaceAll(Grammar):

    grammar = (
        REPLACE_ALL + LPAREN + DelimitedList(expression_proxy, min=3, max=3) + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {'$replaceAll': dict(zip(('input', 'find', 'replacement'), tokens[1:]))}


class Split(Grammar, ExpressionAction):

    grammar = SPLIT + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN


class StrLenBytes(Grammar, ExpressionAction):

    grammar = STR_LEN_BYTES + LPAREN + expression_proxy + RPAREN

    @staticmethod
    def action(tokens):
        return {'$strLenBytes': tokens[1]}


class StrLenCP(Grammar, ExpressionAction):

    grammar = STR_LEN_CP + LPAREN + expression_proxy + RPAREN

    @staticmethod
    def action(tokens):
        return {'$strLenCP': tokens[1]}


class StrCaseCmp(Grammar, ExpressionAction):

    grammar = (
        STR_CASE_CMP + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN
    )

    @classmethod
    def action(cls, tokens):
        return {'$strcasecmp': tokens[1:]}


class Substr(Grammar, ExpressionAction):

    grammar = SUBSTR + LPAREN + DelimitedList(expression_proxy, min=3, max=3) + RPAREN


class SubstrBytes(Grammar, ExpressionAction):

    grammar = (
        SUBSTR_BYTES + LPAREN + DelimitedList(expression_proxy, min=3, max=3) + RPAREN
    )


class SubstrCP(Grammar, ExpressionAction):

    grammar = (
        SUBSTR_CP + LPAREN + DelimitedList(expression_proxy, min=3, max=3) + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {'$substrCP': tokens[1:]}


class ToLower(Grammar, ExpressionAction):

    grammar = TO_LOWER + LPAREN + expression_proxy + RPAREN


class ToUpper(Grammar, ExpressionAction):

    grammar = TO_UPPER + LPAREN + expression_proxy + RPAREN


StringExpression = (
    Concat
    | IndexOfBytes
    | IndexOfCP
    | Trim
    | LTrim
    | RTrim
    | RegexFind
    | RegexFindAll
    | RegexMatch
    | Replace
    | ReplaceAll
    | Split
    | StrCaseCmp
    | StrLenBytes
    | StrLenCP
    | Substr
    | SubstrBytes
    | SubstrCP
    | ToLower
    | ToUpper
)
