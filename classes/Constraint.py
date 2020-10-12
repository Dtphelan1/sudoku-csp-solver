class Constraint():
    def __init__(self, variables, constraint_fn):
        self.variables = variables
        self.constraint_fn = constraint_fn

    def isSatisfied(self):
        return self.constraint_fn(self.variables)

    def getConstrainedGroup(self, variable):
        if (variable in self.variables):
            return [v for v in self.variables if v != variable]
        return []
