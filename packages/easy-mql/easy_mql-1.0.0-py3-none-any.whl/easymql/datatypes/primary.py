from easymql.core import QuotedString, Regex, sci_real, real, signed_integer
from easymql.exc import DatePartOutOfRangeError
from easymql.keywords import null, true, false
from easymql.meta import Grammar
from easymql.utils import safe_cast_int


class PrimaryDataType(Grammar):
    pass


class Null(PrimaryDataType):

    grammar = null

    @classmethod
    def action(cls, tokens):
        return cls(None)

    def __eq__(self, other):
        if super().__eq__(other) is False:
            return isinstance(other, type(None)) and self.value is other
        return True


class String(PrimaryDataType):
    name = 'string'
    grammar = QuotedString(quoteChar='"', escChar='\\', multiline=True)

    @classmethod
    def action(cls, token):
        return cls(token[0])

    def __eq__(self, other):
        if super().__eq__(other) is False:
            return isinstance(other, str) and self.value == other
        return True


class Boolean(PrimaryDataType):

    grammar = true | false

    @classmethod
    def action(cls, token):
        return Boolean(token[0] == 'true')

    def __eq__(self, other):
        if super().__eq__(other) is False:
            return isinstance(other, bool) and self.value == other
        return True


class Integer(PrimaryDataType):
    name = 'integer'
    grammar = signed_integer

    @classmethod
    def action(cls, token):
        return cls(int(token[0]))

    def __eq__(self, other):
        if super().__eq__(other) is False:
            return isinstance(other, int) and self.value == other
        return True


class Decimal(PrimaryDataType):
    name = 'decimal'
    grammar = sci_real | real

    @classmethod
    def action(cls, token):
        return cls(token[0])

    def __eq__(self, other):
        if super().__eq__(other) is False:
            return isinstance(other, float) and self.value == other
        return True


class Number(PrimaryDataType):
    name = 'number'
    grammar = Decimal | Integer


class Date(PrimaryDataType):

    grammar = Regex(
        r'D"(?P<year>\d{4})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?'
        r'([T ](?P<hour>\d{2}):(?P<minute>\d{2})(:(?P<second>\d{2})(\.(?P<millisecond>\d{3}))?)?'
        r'(?P<timezone>(Z|[+-](?P<tzhour>\d{2})(:?(?P<tzminute>\d{2}))?))?)?"'
    )

    range_map = {
        'year': {'min': 0, 'max': 9999},
        'month': {'min': 1, 'max': 12},
        'day': {'min': 1, 'max': 31},
        'hour': {'min': 0, 'max': 23},
        'minute': {'min': 0, 'max': 59},
        'second': {'min': 0, 'max': 59},
        'millisecond': {'min': 0, 'max': 999},
        'tzhour': {'min': -26, 'max': 26},
        'tzminute': {'min': 0, 'max': 59},
    }

    def __init__(
        self,
        year,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
        millisecond=0,
        timezone='Z',
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond
        self.timezone = timezone
        self.tzhour = 0
        self.tzminute = 0
        if 4 < len(timezone) < 7:  # [+-]HH:MM or [+-]HHMM
            self.tzhour = int(timezone[:3])
            self.tzminute = int(timezone[-2:])
        elif len(timezone) == 3:  # [+-]HH
            self.tzhour = int(timezone)

        self.validate()

        super(Date, self).__init__(
            {
                '$dateFromParts': {
                    part: getattr(self, part)
                    for part in [
                        'year',
                        'month',
                        'day',
                        'hour',
                        'minute',
                        'second',
                        'millisecond',
                        'timezone',
                    ]
                }
            }
        )

    def validate(self):
        for part, range in self.range_map.items():
            value = getattr(self, part)
            min, max = range['min'], range['max']
            try:
                if value < min or value > max:
                    raise DatePartOutOfRangeError(
                        f'{part}({value}) is out of range [{min} - {max}]'
                    )
            except TypeError:
                pass

    def __repr__(self):
        arg_str = ', '.join(
            [
                repr(getattr(self, p))
                for p in [
                    'year',
                    'month',
                    'day',
                    'hour',
                    'minute',
                    'second',
                    'millisecond',
                    'timezone',
                ]
            ]
        )
        return f'Date({arg_str})'

    @classmethod
    def action(cls, tokens):
        kwargs = {
            p: safe_cast_int(tokens[p])
            for p in ['year', 'month', 'day', 'hour', 'minute', 'second', 'millisecond']
            if tokens[p] is not None
        }
        if tokens['timezone'] is not None:
            kwargs['timezone'] = tokens['timezone']
        return cls(**kwargs)


Primary = Null | String | Boolean | Number | Integer | Decimal | Date
