from easymql.actions import ExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.identifiers import BINARY_SIZE, BSON_SIZE
from easymql.meta import Grammar
from easymql.proxies import expression_proxy


class BinarySize(Grammar, ExpressionAction):

    grammar = BINARY_SIZE + LPAREN + expression_proxy + RPAREN


class BsonSize(Grammar, ExpressionAction):

    grammar = BSON_SIZE + LPAREN + expression_proxy + RPAREN


DataSizeExpression = BinarySize | BsonSize
