from objects import BuiltIn
from environment import Environment


class PrintFunction(BuiltIn):

    def evaluate(self, str, env):
        print(str)


BUILTINS = Environment()
BUILTINS.set('print', PrintFunction())
