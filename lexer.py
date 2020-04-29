import sly


class Lexer(sly.Lexer):
    tokens = {LET, ASSIGN, IF, ELSE, TRUE, FALSE, FUNC, RETURN, ID, NUM,
              PLUS, MINUS, MULT, DIV, LT, GT, LTE, GTE, LPARAN, RPARAN, LBRACE, RBRACE, COMMA}

    ignore = r'\t'
    ignore_newline = r'\n'
    ignore_whitespace = r' '

    LET = r'let'
    ASSIGN = r'\='
    IF = r'if'
    ELSE = r'else'
    TRUE = r'true'
    FALSE = r'false'
    FUNC = r'func'
    RETURN = r'return'

    ID = r'[a-zA-Z][a-zA-Z0-9_]*'
    NUM = r'[0-9]+'

    PLUS = r'\+'
    MINUS = r'\-'
    MULT = r'\*'
    DIV = r'\/'

    LT = r'<'
    GT = r'>'
    LTE = r'<='
    GTE = r'<='

    LPARAN = r'\('
    RPARAN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COMMA = r'\,'

