from easymql.core import QuotedString, Regex
from easymql.meta import Grammar


class FieldPath(Grammar):
    name = 'field_path'
    grammar = QuotedString(quoteChar="'", escChar='\\') | Regex(r'[\w.]+')

    @classmethod
    def action(cls, token):
        return '$' + token[0]
