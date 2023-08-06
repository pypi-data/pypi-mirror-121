from pyparsing import (
    Empty as PpEmpty,
    Forward as PpForward,
    Keyword as PpKeyword,
    Literal as PpLiteral,
    Suppress as PpSuppress,
    Word as PpWord,
    QuotedString as PpQuotedString,
    Regex as PpRegex,
    Optional as PpOptional,
    White as PpWhite,
    oneOf,
    infixNotation as PpInfixNotation,
    opAssoc as OpAssoc,  # noqa
    MatchFirst as PpMatchFirst,
    And as PpAnd,
    pythonStyleComment,
    pyparsing_common,
)


class Adapter:
    def __init__(self, grammar):
        self.grammar = grammar
        try:
            self._set_parse_action(self.action)
        except AttributeError:
            pass
        try:
            self.set_name(str(self))
        except AttributeError:
            pass

    def _set_parse_action(self, action):
        try:
            self.grammar.setParseAction(action)
        except AttributeError:
            pass

    def set_name(self, name):
        self.grammar.setName(name)

    def __add__(self, other):
        return And([self, other])

    def __radd__(self, other):
        # return Adapter(self.grammar.__radd__(other._grammar))
        return other + self

    def __sub__(self, other):
        return Adapter(self.grammar.__sub__(other._grammar))

    def __rsub__(self, other):
        return other - self

    def __eq__(self, other):
        return self.grammar.__eq__(other._grammar)

    def __req__(self, other):
        return self == other

    def __ne__(self, other):
        return not (self == other)

    def __rne__(self, other):
        return not (self == other)

    def __getitem__(self, key):
        return MultipleMatch(self, key)

    def __mul__(self, other):
        return Adapter(self.grammar.__mul__(other._grammar))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __or__(self, other):
        return MatchFirst([self, other])

    def __ror__(self, other):
        return other | self

    # def __repr__(self):
    #     return f'{self.__class__.__name__}({self.value})'

    def __str__(self):
        return str(self.grammar)

    @property
    def _grammar(self):
        """Return PyParsing grammar contained in this instance."""
        return self.grammar

    def get_adapter_grammar(self):
        return self

    def parse(self, string, explode=True):
        result = self.grammar.parseString(string, parseAll=True).asList()
        if explode and len(result) == 1:
            return result.pop()
        else:
            return result

    def ignore(self, expr):
        return Adapter(self.grammar.ignore(expr._grammar))


class Keyword(Adapter):
    def __init__(self, match_string):
        self.match_string = match_string
        super(Keyword, self).__init__(PpKeyword(match_string))

    def __str__(self):
        return self.match_string


class Word(Adapter):
    def __init__(
        self,
        initChars,
        bodyChars=None,
        min=1,
        max=0,
        exact=0,
        asKeyword=False,
        excludeChars=None,
    ):
        grammar = PpWord(initChars, bodyChars, min, max, exact, asKeyword, excludeChars)
        super(Word, self).__init__(grammar)


class Suppress(Adapter):
    def __init__(self, expr):
        self.expr = expr
        super(Suppress, self).__init__(PpSuppress(expr._grammar))

    def __str__(self):
        return str(self.expr)


class QuotedString(Adapter):
    def __init__(
        self,
        quoteChar,
        escChar=None,
        escQuote=None,
        multiline=False,
        unquoteResults=True,
        endQuoteChar=None,
        convertWhitespaceEscapes=True,
    ):
        grammar = PpQuotedString(
            quoteChar,
            escChar,
            escQuote,
            multiline,
            unquoteResults,
            endQuoteChar,
            convertWhitespaceEscapes,
        )
        super(QuotedString, self).__init__(grammar)


class Forward(Adapter):
    def __init__(self, other=None):
        grammar = PpForward(other)
        super(Forward, self).__init__(grammar)

    def __lshift__(self, other):
        return Adapter(self.grammar.__lshift__(other._grammar))

    def __ilshift__(self, other):
        return Adapter(self.grammar.__ilshift__(other._grammar))


class Regex(Adapter):
    def __init__(self, pattern, flags=0, asGroupList=False, asMatch=False):
        grammar = PpRegex(pattern, flags, asGroupList, asMatch)
        super(Regex, self).__init__(grammar)


class Empty(Adapter):
    def __init__(self):
        super(Empty, self).__init__(PpEmpty())


class Literal(Adapter):
    def __init__(self, match_string):
        self.match_string = match_string
        super(Literal, self).__init__(PpLiteral(match_string))

    def __str__(self):
        return self.match_string


class Optional(Adapter):
    def __init__(self, expr):
        self.expr = expr
        super(Optional, self).__init__(PpOptional(expr._grammar))

    def __str__(self):
        return f'[ {self.expr._grammar} ]'


class White(Adapter):
    def __init__(self, ws=" \t\r\n", min=1, max=0, exact=0):
        super(White, self).__init__(PpWhite(ws, min, max, exact))


class OneOf(Adapter):
    def __init__(self, literals, case_less=False, use_regex=True, as_keyword=False):
        super(OneOf, self).__init__(oneOf(literals, case_less, use_regex, as_keyword))


class InfixExpression(Adapter):
    def __init__(
        self,
        base_expr,
        precedence_list,
        lparen=Suppress(Literal('(')),
        rparen=Suppress(Literal(')')),
    ):
        super(InfixExpression, self).__init__(
            PpInfixNotation(
                base_expr._grammar,
                [(p[0]._grammar, *p[1:]) for p in precedence_list],
                lparen._grammar,
                rparen._grammar,
            )
        )


class ParseExpression(Adapter):
    pass


class MatchFirst(ParseExpression):
    def __init__(self, exprs, savelist=False):
        self.exprs = exprs
        grammar = PpMatchFirst([expr._grammar for expr in exprs], savelist)
        super(MatchFirst, self).__init__(grammar)

    def _get_elements(self):
        """Flatten the nested MatchFirst objects and return as a list.

        { { A | B } | C } will become { A | B | C }.
        """
        res = []
        for expr in self.exprs:
            if isinstance(expr, MatchFirst):
                res += expr._get_elements()
            else:
                res.append(expr)
        return res

    def __str__(self):
        return '{ ' + ' | '.join(str(e._grammar) for e in self._get_elements()) + ' }'


class And(ParseExpression):
    def __init__(self, exprs, savelist=True):
        self.exprs = exprs
        grammar = PpAnd([expr._grammar for expr in exprs], savelist)
        super(And, self).__init__(grammar)

    def __str__(self):
        return ' '.join(str(e._grammar) for e in self.exprs)


class HashComment(Adapter):
    def __init__(self):
        super(HashComment, self).__init__(pythonStyleComment)


class MultipleMatch(Adapter):
    """Unlike others, this class does not use any specific PyParsing class.

    self.grammar here can be pyparsing.OneOrMore or pyparsing.ZeroOrMore.
    This class is created to override str behaviour of those classes.
    """

    def __init__(self, expr, key):
        self.expr = expr
        super(MultipleMatch, self).__init__(expr.grammar[key])

    def __str__(self):
        if isinstance(self.expr.get_adapter_grammar(), And):
            return f'{{ {self.expr._grammar} }}...'
        else:
            return f'{self.expr._grammar}...'


sci_real = Adapter(pyparsing_common.sci_real)
real = Adapter(pyparsing_common.real)
signed_integer = Adapter(pyparsing_common.signed_integer)
