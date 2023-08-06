from easymql.actions import UnaryExpressionAction
from easymql.basics import LPAREN, RPAREN
from easymql.expressions import Expression
from easymql.identifiers import *
from easymql.meta import Grammar


class AddToSet(Grammar, UnaryExpressionAction):

    grammar = ADD_TO_SET + LPAREN + Expression + RPAREN


class Avg(Grammar, UnaryExpressionAction):

    grammar = AVG + LPAREN + Expression + RPAREN


class First(Grammar, UnaryExpressionAction):

    grammar = FIRST + LPAREN + Expression + RPAREN


class Last(Grammar, UnaryExpressionAction):

    grammar = LAST + LPAREN + Expression + RPAREN


class Max(Grammar, UnaryExpressionAction):

    grammar = MAX + LPAREN + Expression + RPAREN


class MergeObjects(Grammar, UnaryExpressionAction):

    grammar = MERGE_OBJECTS + LPAREN + Expression + RPAREN


class Min(Grammar, UnaryExpressionAction):

    grammar = MIN + LPAREN + Expression + RPAREN


class Push(Grammar, UnaryExpressionAction):

    grammar = PUSH + LPAREN + Expression + RPAREN


class StdDevPop(Grammar, UnaryExpressionAction):

    grammar = STD_DEV_POP + LPAREN + Expression + RPAREN


class StdDevSamp(Grammar, UnaryExpressionAction):

    grammar = STD_DEV_SAMP + LPAREN + Expression + RPAREN


class Sum(Grammar, UnaryExpressionAction):

    grammar = SUM + LPAREN + Expression + RPAREN


class AccumulatorExpression(Grammar):

    name = 'accumulator_expression'
    grammar = (
        AddToSet
        | Avg
        | First
        | Last
        | Max
        | MergeObjects
        | Min
        | Push
        | StdDevPop
        | StdDevSamp
        | Sum
    )
