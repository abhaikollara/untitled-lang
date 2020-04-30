from objects import BuiltIn


class PrintFunction(BuiltIn):
    
    def evaluate(self, str, env):
        print(str)


BUILTINS = {
    'print': PrintFunction()
    }