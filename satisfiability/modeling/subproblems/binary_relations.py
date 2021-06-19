from satisfiability.modeling.problem import SatFormula, SatProblem


class Distinct(SatFormula):
    def __init__(self, root: SatProblem, l1, l2):
        super().__init__()
        self.add_clause(+l1, +l2)
        self.add_clause(-l1, -l2)


class Equal(SatFormula):
    def __init__(self, root: SatProblem, l1, l2):
        super().__init__()
        self.add_clause(+l1, -l2)
        self.add_clause(-l1, +l2)


class Implies(SatFormula):
    def __init__(self, root: SatProblem, l1, l2):
        super().__init__()
        self.add_clause(-l1, +l2)
