from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.identifiers import CMP
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class Cmp(Grammar, ExpressionAction):

    grammar = CMP + LPAREN + DelimitedList(expression_proxy, min=2, max=2) + RPAREN
