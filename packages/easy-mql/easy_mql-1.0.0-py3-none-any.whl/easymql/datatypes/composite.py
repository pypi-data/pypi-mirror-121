from functools import reduce

from easymql.basics import *
from easymql.core import QuotedString
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class Array(Grammar):

    grammar = LBRACK + DelimitedList(expression_proxy, min=0, max=...) + RBRACK

    @classmethod
    def action(cls, tokens):
        return [tokens.asList()]


class KeyValuePair(Grammar):

    grammar = QuotedString(quoteChar='"', escChar='\\') + COLON + expression_proxy

    @classmethod
    def action(cls, tokens):
        return {tokens[0]: tokens[1]}


class Object(Grammar):

    grammar = LBRACE + DelimitedList(KeyValuePair, min=0, max=...) + RBRACE

    @classmethod
    def action(cls, tokens):
        return reduce(lambda e1, e2: {**e1, **e2}, tokens) if tokens else {}


Composite = Array | Object
