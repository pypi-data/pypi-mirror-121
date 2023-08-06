from easymql.actions import ExpressionAction, UnaryExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.datatypes.primary import Decimal
from easymql.identifiers import RANDOM, SAMPLE_RATE
from easymql.meta import Grammar


class Random(Grammar, ExpressionAction):

    grammar = RANDOM + LPAREN + RPAREN

    @staticmethod
    def action(tokens):
        return {'$rand': {}}


class SampleRate(Grammar, UnaryExpressionAction):

    grammar = SAMPLE_RATE + LPAREN + Decimal + RPAREN


MiscellaneousExpression = Random | SampleRate
