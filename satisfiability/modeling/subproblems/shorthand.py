from satisfiability.modeling.problem import SatFormula, SatProblem


class AllOf(SatFormula):
    def __init__(self, root: SatProblem, *literals):
        super().__init__()
        for literal in literals:
            self.add_clause(literal)


class NoneOf(SatFormula):
    def __init__(self, root: SatProblem, *literals):
        super().__init__()
        for literal in literals:
            self.add_clause(-literal)
