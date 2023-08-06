from pyparsing import ParserElement

ParserElement.enablePackrat()


class MetaGrammar(type):
    def __init__(cls, name, bases, dct):
        super(MetaGrammar, cls).__init__(name, bases, dct)
        try:
            cls._set_parse_action(cls.action)
        except AttributeError as e:
            pass
        try:
            cls.set_name(cls.name)
        except AttributeError as e:
            pass

    def __add__(cls, other):
        return cls.grammar.__add__(other)

    def __and__(cls, other):
        return cls.grammar.__and__(other)

    # def __eq__(cls, other):
    #     return cls.grammar.__eq__(other)

    def __getitem__(cls, key):
        return cls.grammar[key]

    def __mul__(cls, other):
        return cls.grammar.__mul__(other)

    # def __ne__(cls, other):
    #     return cls.grammar.__ne__(other)

    def __or__(cls, other):
        return cls.grammar.__or__(other)

    def __radd__(cls, other):
        return cls.grammar.__radd__(other)

    def __rand__(cls, other):
        return cls.grammar.__rand__(other)

    def __req__(cls, other):
        return cls.grammar.__req__(other)

    def __rmul__(cls, other):
        return cls.grammar.__rmul__(other)

    def __rne__(cls, other):
        return cls.grammar.__rne__(other)

    def __ror__(cls, other):
        return cls.grammar.__ror__(other)

    def __rsub__(cls, other):
        return cls.grammar.__rsub__(other)

    def __rxor__(cls, other):
        return cls.grammar.__rxor__(other)

    def __sub__(cls, other):
        return cls.grammar.__sub__(other)

    def __xor__(cls, other):
        return cls.grammar.__xor__(other)

    def get_adapter_grammar(cls):
        return cls.grammar.get_adapter_grammar()

    @property
    def _grammar(cls):
        """Return pyparsing grammar contained in this class travelling
        from MetaGrammar --> Grammar --> Adapter --> PyParsing
        """
        return cls.grammar._grammar

    def ignore(cls, expr):
        return cls._grammar.ignore(expr)

    def _set_parse_action(cls, action):
        try:
            cls.grammar._set_parse_action(action)
        except AttributeError:
            pass

    def parse(cls, string, explode=True):
        return cls.grammar.parse(string, explode)

    def set_name(cls, name):
        try:
            cls.grammar.set_name(name)
        except AttributeError:
            pass


class Grammar(metaclass=MetaGrammar):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.value)})"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __ne__(self, other):
        return not self == other
