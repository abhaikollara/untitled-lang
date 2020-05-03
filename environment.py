class Environment:

    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def get(self, sym):
        try:
            return self.bindings[sym]
        except KeyError:
            if self.parent is not None:
                return self.parent.get(sym)

            raise ValueError(f"Unbound symbol {sym}")

    def set(self, sym, value):
        self.bindings[sym] = value

    def merge(self, other):
        self.bindings.update(other.bindings)

    def __repr__(self):
        return repr(self.bindings)
