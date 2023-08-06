from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.identifiers import MERGE_OBJECTS, OBJECT_TO_ARRAY
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class MergeObjects(Grammar, ExpressionAction):

    grammar = MERGE_OBJECTS + LPAREN + DelimitedList(expression_proxy) + RPAREN


class ObjectToArray(Grammar):

    grammar = OBJECT_TO_ARRAY + LPAREN + expression_proxy + RPAREN

    @classmethod
    def action(cls, tokens):
        return {'$objectToArray': tokens[1]}
