import operator

from lexer import Lexer
from parser import Parser
import ast_
import objects


class Environment:

    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def get_symbol(self, sym):
        try:
            return self.bindings[sym]
        except KeyError:
            if self.parent is not None:
                return self.parent.get_symbol(sym)

            raise ValueError(f"Unbound symbol {sym}")

    def add(self, sym, value):
        self.bindings[sym] = value
    
    def __repr__(self):
        return repr(self.bindings)


class Evaluator:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()

    def evaluate(self, node, env):
        if isinstance(node, ast_.Block):
            return self.evaluate_block(node, env)
        elif isinstance(node, ast_.IntLiteral):
            return self.evaluate_int_literal(node, env)
        elif isinstance(node, ast_.BoolLiteral):
            return self.evaluate_bool_literal(node, env)
        elif isinstance(node, ast_.Assignment):
            return self.evaluate_assignment(node, env)
        elif isinstance(node, ast_.Conditional):
            return self.evaluate_conditional(node, env)
        elif isinstance(node, ast_.FunctionDef):
            return self.evaluate_function_def(node, env)
        elif isinstance(node, ast_.FunctionCall):
            return self.evaluate_function_call(node, env)
        elif isinstance(node, ast_.Identifier):
            return self.evaluate_identifier(node, env)
        elif isinstance(node, ast_.Return):
            return self.evaluate_return(node, env)
        elif isinstance(node, ast_.BinOp):
            return self.evaluate_binop(node, env)
        else:
            raise TypeError("AST Node invalid")

    def evaluate_block(self, node, env):
        # TODO : Create new env ?
        # nenv = Environment(parent=env)
        for stmt in node.stmts:
            last = self.evaluate(stmt, env)
            if isinstance(last, objects.Returned):
                return last
        
        return objects.Returned(objects.NIL)

    def evaluate_int_literal(self, node, env):
        return objects.Integer(int(node.value))

    def evaluate_bool_literal(self, node, env):
        if node.value == 'true':
            return objects.TRUE
        else:
            return objects.FALSE

    def evaluate_assignment(self, node, env):
        value = self.evaluate(node.expr, env)
        env.add(node.id, value)

    @staticmethod
    def is_truthy(value):
        if value == objects.TRUE:
            return True
        if isinstance(value, objects.Integer):
            return value.value == 0
        
        return False

    def evaluate_conditional(self, node, env):
        if Evaluator.is_truthy(self.evaluate(node.cond, env)) is True:
            return self.evaluate(node.cons, env)
        elif node.alt is not None:
            return self.evaluate(node.alt, env)
    
    def evaluate_function_def(self, node, env):
        func = objects.Function(node.id, node.params, node.body, env)
        env.add(node.id, func)

    def evaluate_function_call(self, node, env):
        func = env.get_symbol(node.id)
        if not isinstance(func, objects.Function):
            raise TypeError(f"Expected function, found {func} of type {type(func)}")

        new_env = Environment(parent=env)
        new_env.bindings.update(func.env.bindings)
        for param,arg in zip(func.params, node.args):
            new_env.add(param, self.evaluate(arg, env))

        return self.evaluate_block(func.body, new_env).value


    def evaluate_return(self, node, env):
        rval = self.evaluate(node.expr, env)

        return objects.Returned(rval)

    @staticmethod
    def select_op(op):
        if op == '+':
            return operator.add
        if op == '-':
            return operator.sub
        if op == '*':
            return operator.mul
        if op == '/':
            return operator.floordiv
        if op == '>':
            return operator.gt
        if op == '<':
            return operator.lt
        if op == '>=':
            return operator.gte
        if op == '<=':
            return operator.lte
        if op == '==':
            return operator.eq
        if op == '!=':
            return operator.ne

    def evaluate_binop(self, node, env):
        op = Evaluator.select_op(node.op)
        lhs = self.evaluate(node.left, env)
        rhs = self.evaluate(node.right, env)

        return op(lhs, rhs)

    def evaluate_identifier(self, ident, env):
        return env.get_symbol(ident.name)

    def eval_program(self, program):
        env = Environment()
        for stmt in program.stmts:
            last = self.evaluate(stmt, env)
            if last is not None:
                print(last)

    def eval_source(self, source):
        tokens = self.lexer.tokenize(source)
        program = self.parser.parse(tokens)

        return self.eval_program(program)
