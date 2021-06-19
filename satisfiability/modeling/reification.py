from satisfiability.modeling.primitives import Literal
from satisfiability.modeling.problem import SatFormula


class PartiallyReified(SatFormula):
    # this is a bit awkward. I'm not sure if this is a symptom of SAT or the model itself
    def __init__(self, reifier: Literal, formula: SatFormula):
        super().__init__()
        self.reifier = reifier
        self.formula = formula

    @property
    def clauses(self):
        for clause in self.formula.clauses:
            yield (-self.reifier,)+clause

    @property
    def qt_clauses(self):
        return self.formula.qt_clauses
