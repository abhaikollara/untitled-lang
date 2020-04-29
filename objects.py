class Object: pass

class Integer(Object):
    def __init__(self, value):
        self.value = value
    
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

    def __init__(self, name, body, env):
        self.name = name
        self.body = body
        self.env = env
    
    def __repr__(self):
        return f"Function({self.name})"