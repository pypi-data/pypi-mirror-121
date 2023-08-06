from easymql.basics import LPAREN, RPAREN, COMMA
from easymql.core import Keyword, MatchFirst, Optional, Suppress
from easymql.datatypes.primary import Null
from easymql.identifiers import DATE, ISO_WEEK_DATE, PARSE_DATE, FORMAT_DATE, EXTRACT
from easymql.meta import Grammar
from easymql.proxies import expression_proxy
from easymql.utils import DelimitedList


class DateFunc(Grammar):

    grammar = (
        Suppress(DATE) + LPAREN + DelimitedList(expression_proxy, min=1, max=8) + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {
            '$dateFromParts': dict(
                zip(
                    [
                        'year',
                        'month',
                        'day',
                        'hour',
                        'minute',
                        'second',
                        'millisecond',
                        'timezone',
                    ],
                    tokens,
                )
            )
        }


class IsoWeekDateFunc(Grammar):

    grammar = (
        Suppress(ISO_WEEK_DATE)
        + LPAREN
        + DelimitedList(expression_proxy, min=1, max=8)
        + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {
            '$dateFromParts': dict(
                zip(
                    [
                        'isoWeekYear',
                        'isoWeek',
                        'isoDayOfWeek',
                        'hour',
                        'minute',
                        'second',
                        'millisecond',
                        'timezone',
                    ],
                    tokens,
                )
            )
        }


class ParseDate(Grammar):

    grammar = (
        PARSE_DATE + LPAREN + DelimitedList(expression_proxy, min=1, max=3) + RPAREN
    )

    @staticmethod
    def action(tokens):
        print(tokens)
        doc = {'dateString': tokens[1]}
        # Add 'format' to result only if it is not 'null'
        if len(tokens) >= 3 and not isinstance(tokens[2], Null):
            doc['format'] = tokens[2]
        if len(tokens) == 4:
            doc['timezone'] = tokens[3]
        return {'$dateFromString': doc}


class FormatDate(Grammar):

    grammar = (
        FORMAT_DATE + LPAREN + DelimitedList(expression_proxy, min=1, max=3) + RPAREN
    )

    @staticmethod
    def action(tokens):
        print(tokens)
        doc = {'date': tokens[1]}
        # Add 'format' to result only if it is not 'null'
        if len(tokens) >= 3 and not isinstance(tokens[2], Null):
            doc['format'] = tokens[2]
        if len(tokens) == 4:
            doc['timezone'] = tokens[3]
        return {'$dateToString': doc}


class Extract(Grammar):

    date_part_map = {
        'MILLISECOND': '$millisecond',
        'SECOND': '$second',
        'MINUTE': '$minute',
        'HOUR': '$hour',
        'DAY_OF_WEEK': '$dayOfWeek',
        'ISO_DAY_OF_WEEK': '$isoDayOfWeek',
        'DAY_OF_MONTH': '$day',
        'DAY_OF_YEAR': '$dayOfYear',
        'WEEK': '$week',
        'ISO_WEEK': '$isoWeek',
        'MONTH': '$month',
        'YEAR': '$year',
        'ISO_YEAR': '$isoYear',
    }
    grammar = (
        EXTRACT
        + LPAREN
        + MatchFirst(map(Keyword, date_part_map.keys()))
        + COMMA
        + expression_proxy
        + Optional(COMMA + expression_proxy)
        + RPAREN
    )

    @staticmethod
    def action(tokens):
        return {
            Extract.date_part_map[tokens[1]]: dict(
                zip(('date', 'timezone'), tokens[2:])
            )
        }


DateExpression = DateFunc | IsoWeekDateFunc | ParseDate | FormatDate | Extract
