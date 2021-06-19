from enum import Enum

from satisfiability.modeling.problem import SatProblem, SatFormula
from satisfiability.modeling.subproblems.binary_relations import Equal


class OrderType(Enum):
    BOTH = 1
    LOWER = 2
    UPPER = 3


class Comparator(SatFormula):
    def __init__(self, root: SatProblem, i1, i2, o1, o2, kind=OrderType.BOTH):
        super().__init__()
        if kind != OrderType.UPPER:
            self.add_clause(+i1, -o2)
            self.add_clause(+i2, -o2)
            self.add_clause(+i1, +i2, -o1)
        if kind != OrderType.LOWER:
            self.add_clause(-i1, +o1)
            self.add_clause(-i2, +o1)
            self.add_clause(-i1, -i2, +o2)


class MergeNetwork(SatFormula):
    def __init__(self, root: SatProblem, order, inputs, outputs, kind=OrderType.BOTH):
        super().__init__()

        if order == 1:
            self.add_subproblem(Comparator(root, *inputs, *outputs, kind=kind))
            return

        qt_items = 2**order
        if len(inputs) != qt_items or len(outputs) != qt_items:
            raise Exception("MergeNetwork got an incorrect amount of inputs or outputs")

        half_merges = [root.new_var() for _ in range(qt_items)]
        self.add_subproblem(MergeNetwork(root, order-1, inputs[0::2], half_merges[0::2], kind=kind))
        self.add_subproblem(MergeNetwork(root, order-1, inputs[1::2], half_merges[1::2], kind=kind))
        self.add_subproblem(Equal(root, half_merges[0], outputs[0]))
        for i in range(1, qt_items-1, 2):
            self.add_subproblem(Comparator(root, half_merges[i], half_merges[i+1], outputs[i], outputs[i+1], kind=kind))
        self.add_subproblem(Equal(root, half_merges[-1], outputs[-1]))


class SortingNetwork(SatFormula):
    def __init__(self, root: SatProblem, order, inputs, outputs, kind=OrderType.BOTH):
        super().__init__()

        if order == 1:
            self.add_subproblem(Comparator(root, *inputs, *outputs, kind=kind))
            return

        qt_items = 2**order
        if len(inputs) != qt_items or len(outputs) != qt_items:
            raise Exception("MergeNetwork got an incorrect amount of inputs or outputs")

        halfway = 2**(order-1)
        half_sorts = [root.new_var() for _ in range(qt_items)]
        self.add_subproblem(SortingNetwork(root, order-1, inputs[:halfway], half_sorts[:halfway], kind=kind))
        self.add_subproblem(SortingNetwork(root, order-1, inputs[halfway:], half_sorts[halfway:], kind=kind))
        self.add_subproblem(MergeNetwork(root, order, half_sorts, outputs, kind=kind))

    @classmethod
    def generic_constructor(cls, root: SatProblem, inputs, outputs, kind=OrderType.BOTH):
        # there might be a better way to do this...
        if len(inputs) != len(outputs):
            raise Exception("MergeNetwork mismatch on amount of inputs/outputs")
        order = 1
        cardinality = 2
        while cardinality < len(inputs):
            order += 1
            cardinality *= 2
        problem = SatFormula()
        for _ in range(len(inputs), cardinality):
            inputs.append(root.new_var())
            problem.add_clause(-inputs[-1])
            outputs.append(root.new_var())
        problem.add_subproblem(SortingNetwork(root, order, inputs, outputs, kind=kind))
        return problem


class Exactly(SatFormula):
    def __init__(self, root: SatProblem, inputs, k):
        super().__init__()
        outputs = [root.new_var() for _ in range(len(inputs))]
        self.add_subproblem(SortingNetwork.generic_constructor(root, inputs, outputs, kind=OrderType.BOTH))
        if k > 0:
            self.add_clause(+outputs[k-1])
        if k < len(inputs):
            self.add_clause(-outputs[k])


class AtLeast(SatFormula):
    def __init__(self, root: SatProblem, inputs, k):
        super().__init__()
        outputs = [root.new_var() for _ in range(len(inputs))]
        self.add_subproblem(SortingNetwork.generic_constructor(root, inputs, outputs, kind=OrderType.LOWER))
        if k > 0:
            self.add_clause(+outputs[k-1])


class AtMost(SatFormula):
    def __init__(self, root: SatProblem, inputs, k):
        super().__init__()
        outputs = [root.new_var() for _ in range(len(inputs))]
        self.add_subproblem(SortingNetwork.generic_constructor(root, inputs, outputs, kind=OrderType.UPPER))
        if k < len(inputs):
            self.add_clause(-outputs[k])