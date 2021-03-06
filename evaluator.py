import operator

from lexer import Lexer
from parser import Parser
import ast_
import objects
import builtins_
from environment import Environment


class Evaluator:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()

    def evaluate(self, node, env):
        if isinstance(node, ast_.Block):
            return self.evaluate_block(node, env)
        elif isinstance(node, ast_.NumLiteral):
            return self.evaluate_num_literal(node, env)
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

    def evaluate_num_literal(self, node, env):
        try:
            value = int(node.value)
        except ValueError:
            value = float(node.value)
        return objects.Number(value)

    def evaluate_bool_literal(self, node, env):
        if node.value == 'true':
            return objects.TRUE
        else:
            return objects.FALSE

    def evaluate_assignment(self, node, env):
        value = self.evaluate(node.expr, env)
        env.set(node.id, value)

    @staticmethod
    def is_truthy(value):
        if value == objects.TRUE:
            return True
        if isinstance(value, objects.Number):
            return value.value == 0

        return False

    def evaluate_conditional(self, node, env):
        if Evaluator.is_truthy(self.evaluate(node.cond, env)) is True:
            return self.evaluate(node.cons, env)
        elif node.alt is not None:
            return self.evaluate(node.alt, env)

    def evaluate_function_def(self, node, env):
        func = objects.Function(node.id, node.params, node.body, env)
        env.set(node.id, func)

    def evaluate_function_call(self, node, env):
        func = env.get(node.id)
        if isinstance(func, objects.BuiltIn):
            return self.evaluate_builtin(func, node.args, env)
        if not isinstance(func, objects.Function):
            raise TypeError(
                f"Expected function, found {func} of type {type(func)}")

        new_env = Environment(parent=env)
        new_env.merge(func.env)

        if len(func.params) != len(node.args):
            raise ValueError(f"`{str(func.name)}` takes {len(func.params)} arguments, but were given {len(node.args)}")
        for param, arg in zip(func.params, node.args):
            new_env.set(param, self.evaluate(arg, env))

        return self.evaluate_block(func.body, new_env).value #TODO: There should be a cleaner way

    def evaluate_builtin(self, func, args, env):
        if isinstance(func, builtins_.PrintFunction):
            return func.evaluate(self.evaluate(args[0], env), env)

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
        return env.get(ident.name)

    def eval_program(self, program):
        env = Environment()
        env.merge(builtins_.BUILTINS)
        for stmt in program.stmts:
            last = self.evaluate(stmt, env)

    def eval_source(self, source):
        tokens = self.lexer.tokenize(source)
        program = self.parser.parse(tokens)

        return self.eval_program(program)
