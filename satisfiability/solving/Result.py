class Result:
    def __init__(self, timed_out, is_satisfiable, assignments):
        self.timed_out = timed_out
        self.is_satisfiable = is_satisfiable
        self.assignments = assignments

    @classmethod
    def satisfiable(cls, assignments):
        return cls(False, True, assignments)

    @classmethod
    def unsatisfiable(cls):
        return cls(False, False, None)

    @classmethod
    def timed_out(cls):
        return cls(True, None, None)

    def __getitem__(self, key):
        return self.assignments[key]