from easymql.core import InfixExpression, OpAssoc, OneOf, Keyword
from easymql.datatypes import DataType
from easymql.expressions.accumulators import AccumulatorExpression
from easymql.expressions.arithmetic import ArithmeticExpression
from easymql.expressions.array import ArrayExpression
from easymql.expressions.comparison import Cmp
from easymql.expressions.conditional import ConditionalExpression
from easymql.expressions.datasize import DataSizeExpression
from easymql.expressions.date import DateExpression
from easymql.expressions.miscellaneous import MiscellaneousExpression
from easymql.expressions.object import MergeObjects, ObjectToArray
from easymql.expressions.others import FieldPath
from easymql.expressions.set import SetExpression
from easymql.expressions.strings import StringExpression
from easymql.expressions.systemvariables import SystemVariables
from easymql.expressions.trigonometry import TrigonometryExpression
from easymql.expressions.type import TypeExpression
from easymql.meta import Grammar
from easymql.proxies import expression_proxy


class FuncExpression(Grammar):

    # Order matters. Especially FieldPath; it should be at the end.
    grammar = (
        DataType
        | AccumulatorExpression
        | ArithmeticExpression
        | ArrayExpression
        | ConditionalExpression
        | Cmp
        | DataSizeExpression
        | DateExpression
        | MiscellaneousExpression
        | MergeObjects
        | ObjectToArray
        | SetExpression
        | TrigonometryExpression
        | TypeExpression
        | StringExpression
        | SystemVariables
        | FieldPath
    )


def infix_action(tokens):
    tokens = tokens[0]

    # op : (op_name, -1 means any)
    # op_name = mongo operator name
    # nterms = no of expressions/terms the operator takes. -1 means any number of terms.
    op_map = {
        '+': ('$add', -1),
        '-': ('$subtract', 2),
        '*': ('$multiply', -1),
        '/': ('$divide', 2),
        '%': ('$mod', 2),
        '>': ('$gt', 2),
        '>=': ('$gte', 2),
        '<': ('$lt', 2),
        '<=': ('$lte', 2),
        '=': ('$eq', 2),
        '!=': ('$ne', 2),
        'AND': ('$and', -1),
        'OR': ('$or', -1),
    }

    res = tokens[0]
    previous_operator = None

    for i in range(1, len(tokens), 2):
        operator = tokens[i]
        right_arg = tokens[i + 1]
        op_name, nterms = op_map[operator]

        # to flatten operators with nterms = -1
        if nterms == -1 and operator == previous_operator:
            res[op_name].append(right_arg)
        else:  # nterms = 2
            res = {op_name: [res, right_arg]}

        previous_operator = operator

    return res


class Expression(Grammar):

    grammar = expression_proxy
    grammar <<= InfixExpression(
        FuncExpression,
        [
            (Keyword('NOT'), 1, OpAssoc.RIGHT, lambda token: {'$not': [token[0][-1]]}),
            (OneOf('* / %'), 2, OpAssoc.LEFT, infix_action),
            (OneOf('+ -'), 2, OpAssoc.LEFT, infix_action),
            (OneOf('< <= > >= = !='), 2, OpAssoc.LEFT, infix_action),
            (OneOf('AND OR', as_keyword=True), 2, OpAssoc.LEFT, infix_action),
        ],
    )
