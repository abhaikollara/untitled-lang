
class Statement:
    pass


class Expression:
    pass


class Program:

    def __init__(self, stmts):
        self.stmts = stmts

    def __repr__(self):
        N = '\n'
        return f"Program([{N.join([repr(s) for s in self.stmts])}])"


class Block:

    def __init__(self, stmts):
        self.stmts = stmts

    def __repr__(self):
        N = '\n'
        return f"Block([{N.join([repr(s) for s in self.stmts])}])"


class Assignment(Statement):

    def __init__(self, ident, expr):
        self.id = ident
        self.expr = expr

    def __repr__(self):
        return f"Assign({self.id}, {self.expr})"


class Return(Statement):

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Return({self.expr})"


class Conditional(Statement):

    def __init__(self, cond, cons, alt):
        self.cond = cond
        self.cons = cons
        self.alt = alt

    def __repr__(self):
        return f"Conditional({repr(self.cond)},\n\t\t{repr(self.cons)},\n\t\t{repr(self.alt)})"


class FunctionDef(Statement):

    def __init__(self, ident, params, body):
        self.id = ident
        self.params = params
        self.body = body

    def __repr__(self):
        return f"Function({self.id})"


class FunctionCall(Expression):

    def __init__(self, ident, args):
        self.id = ident
        self.args = args

    def __repr__(self):
        return f"Call({repr(self.id)})"


class Identifier(Expression):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class BinOp(Expression):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOp({repr(self.left)} {self.op} {repr(self.right)})"


class NumLiteral(Expression):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Num({self.value})"


class BoolLiteral(Expression):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Bool({self.value})"


TRUE = BoolLiteral("true")
FALSE = BoolLiteral("false")
