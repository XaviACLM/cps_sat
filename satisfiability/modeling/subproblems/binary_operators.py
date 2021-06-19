from satisfiability.modeling.problem import SatFormula, SatProblem


class Nor(SatFormula):
    def __init__(self, root: SatProblem, i1, i2, o):
        super().__init__()
        self.add_clause(-i1, -o)
        self.add_clause(-i2, -o)
        self.add_clause(i1, i2, o)


class Nand(SatFormula):
    def __init__(self, root: SatProblem, i1, i2, o):
        super().__init__()
        self.add_clause(i1, o)
        self.add_clause(i2, o)
        self.add_clause(-i1, -i2, -o)
