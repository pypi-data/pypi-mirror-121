from easymql.core import Suppress, Literal


(
    LPAREN,
    RPAREN,
    LBRACE,
    RBRACE,
    LBRACK,
    RBRACK,
    COLON,
    SEMICOLON,
    COMMA,
    PERIOD,
    HYPHEN,
    EQUALS,
) = map(Suppress, map(Literal, tuple('(){}[]:;,.-=')))
