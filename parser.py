import sly
from lexer import Lexer
import ast_


class Parser(sly.Parser):
    tokens = Lexer.tokens
    precedence = (
        ('nonassoc', LT, LTE, GT, GTE),
        ('left', PLUS, MINUS),
        ('left', MULT, DIV))

    start = 'program'

    @_('stmts')
    def program(self, p):
        return ast_.Program(p.stmts)

    @_('LBRACE stmts RBRACE')
    def block(self, p):
        return ast_.Block(p.stmts)

    @_('LBRACE RBRACE')
    def block(self, p):
        return ast_.Block([])

    @_("stmt stmts")
    def stmts(self, p):
        return [p.stmt] + p.stmts

    @_("stmt")
    def stmts(self, p):
        return [p.stmt]

    #  Types of statements

    @_("assignment")
    def stmt(self, p):
        return p.assignment

    @_("return_")
    def stmt(self, p):
        return p.return_

    @_("conditional")
    def stmt(self, p):
        return p.conditional

    @_("func_def")
    def stmt(self, p):
        return p.func_def

    # @_("expr")
    # def stmt(self, p):
    #     return p.expr

    # Actual statements

    @_("LET ID ASSIGN expr")
    def assignment(self, p):
        return ast_.Assignment(p.ID, p.expr)

    @_("RETURN expr")
    def return_(self, p):
        return ast_.Return(p.expr)

    # If Else

    @_("IF condition block else_part")
    def conditional(self, p):
        if p.else_part is None:
            return ast_.Conditional(p.condition, p.block, None)

        return ast_.Conditional(p.condition, p.block, p.else_part)

    @_("expr")
    def condition(self, p):
        return p.expr

    @_("ELSE block")
    def else_part(self, p):
        return p.block

    @_("")
    def else_part(self, p):
        return None

    # Function def

    @_("FUNC ID LPARAN params_list RPARAN block")
    def func_def(self, p):
        return ast_.FunctionDef(p.ID, p.params_list, p.block)

    @_("ID COMMA params_list")
    def params_list(self, p):
        return [p.ID] + p.params_list

    @_("ID")
    def params_list(self, p):
        return [p.ID]

    # Expressions
    @_("ID LPARAN args_list RPARAN")
    def expr(self, p):
        return ast_.FunctionCall(p.ID, p.args_list)

    @_("expr COMMA args_list")
    def args_list(self, p):
        return [p.expr] + p.args_list

    @_("expr")
    def args_list(self, p):
        return [p.expr]

    @_('LPARAN expr RPARAN')
    def expr(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return ast_.BinOp('+', p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return ast_BinOp('-', p.expr0, p.expr1)

    @_('expr MULT expr')
    def expr(self, p):
        return ast_.BinOp('*', p.expr0, p.expr1)

    @_('expr DIV expr')
    def expr(self, p):
        return ast_.BinOp('/', p.expr0, p.expr1)

    @_('expr LT expr')
    def expr(self, p):
        return ast_.BinOp('<', p.expr0, p.expr1)

    @_('expr GT expr')
    def expr(self, p):
        return ast_.BinOp('>', p.expr0, p.expr1)

    @_('expr LTE expr')
    def expr(self, p):
        return ast_.BinOp('<=', p.expr0, p.expr1)

    @_('expr GTE expr')
    def expr(self, p):
        return ast_.BinOp('>=', p.expr0, p.expr1)

    @_('expr EQ expr')
    def expr(self, p):
        return ast_.BinOp('==', p.expr0, p.expr1)

    @_('expr NEQ expr')
    def expr(self, p):
        return ast_.BinOp('!=', p.expr0, p.expr1)

    @_('NUM')
    def expr(self, p):
        return ast_.IntLiteral(p.NUM)

    @_('TRUE')
    def expr(self, p):
        return ast_.TRUE

    @_('FALSE')
    def expr(self, p):
        return ast_.FALSE

    @_('ID')
    def expr(self, p):
        return ast_.Identifier(p.ID)
