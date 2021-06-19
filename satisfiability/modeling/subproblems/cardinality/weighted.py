from satisfiability.modeling.problem import SatFormula, SatProblem
from satisfiability.modeling.subproblems.cardinality.general import SortingNetwork, OrderType
from satisfiability.utils import iter_repeat


class WeightedExactly(SatFormula):
    def __init__(self, root: SatProblem, inputs, weights, k):
        super().__init__()
        inputs = list(iter_repeat(inputs, weights))
        outputs = [root.new_var() for _ in range(len(inputs))]
        self.add_subproblem(SortingNetwork.generic_constructor(root, inputs, outputs, kind=OrderType.BOTH))
        if k > 0:
            self.add_clause(+outputs[k-1])
        if k < len(inputs):
            self.add_clause(-outputs[k])


class WeightedAtLeast(SatFormula):
    def __init__(self, root: SatProblem, inputs, weights, k):
        super().__init__()
        inputs = list(iter_repeat(inputs, weights))
        outputs = [root.new_var() for _ in range(len(inputs))]
        self.add_subproblem(SortingNetwork.generic_constructor(root, inputs, outputs, kind=OrderType.LOWER))
        if k > 0:
            self.add_clause(+outputs[k-1])


class WeightedAtMost(SatFormula):
    def __init__(self, root: SatProblem, inputs, weights, k):
        super().__init__()
        inputs = list(iter_repeat(inputs, weights))
        outputs = [root.new_var() for _ in range(len(inputs))]
        self.add_subproblem(SortingNetwork.generic_constructor(root, inputs, outputs, kind=OrderType.UPPER))
        if k < len(inputs):
            self.add_clause(-outputs[k])