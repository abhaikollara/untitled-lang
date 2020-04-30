class Object: pass

class Integer(Object):
    def __init__(self, value):
        self.value = value
    
    def __add__(self, other):
        return Integer(self.value + other.value)
    
    def __sub__(self, other):
        return Integer(self.value - other.value)
    
    def __mul__(self, other):
        return Integer(self.value * other.value)
    
    def __div__(self, other):
        return Integer(self.value // other.value)

    def __gt__(self, other):
        if self.value > other.value:
            return TRUE
        return FALSE

    def __lt__(self, other):
        if self.value < other.value:
            return TRUE
        return FALSE

    def __ge__(self, other):
        if self.value >= other.value:
            return TRUE
        return FALSE

    def __le__(self, other):
        if self.value <= other.value:
            return TRUE
        return FALSE

    def __eq__(self, other):
        if self.value == other.value:
            return TRUE
        return FALSE

    def __ne__(self, other):
        if self.value != other.value:
            return TRUE
        return FALSE

    def __repr__(self):
        return f"Integer({self.value})"

    def __str__(self):
        return str(self.value)

class Boolean(Object):

    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Boolean({self.value})"
    
    def __str__(self):
        return str(self.value)

TRUE = Boolean("true")
FALSE = Boolean("false")

class Function(Object):

    def __init__(self, name, params, body, env):
        self.name = name
        self.params = params
        self.body = body
        self.env = env
    
    def __repr__(self):
        return f"Function({self.name})"


class Returned(Object):

    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Returned({self.value})"

class Nil(Object):

    def __repr__(self):
        return f"<NIL>"

NIL = Nil()