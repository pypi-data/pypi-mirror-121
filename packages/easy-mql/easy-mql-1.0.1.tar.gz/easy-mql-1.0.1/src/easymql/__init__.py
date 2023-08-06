from pyparsing import ParseException

from easymql.exc import EasyMQLSyntaxError
from easymql.pipeline import Pipeline, encode


class EasyMQL:
    def parse(self, query_string):
        try:
            return encode(Pipeline.parse(query_string, explode=False))
        except ParseException as e:
            raise EasyMQLSyntaxError(query_string, str(e), e.lineno, e.col) from None
