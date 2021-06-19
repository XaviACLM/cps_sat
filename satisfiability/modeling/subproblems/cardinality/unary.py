from satisfiability.modeling.problem import SatFormula, SatProblem


class AtLeastOne(SatFormula):
    def __init__(self, root: SatProblem, *v):
        super().__init__()
        self.add_clause(*v)


class HeuleEncoding(SatFormula):
    def __init__(self, root: SatProblem, *v):
        super().__init__()
        if len(v) <= 3:
            for i in range(len(v)):
                for j in range(i):
                    self.add_clause(-v[i], -v[j])
            return
        v1 = v[:len(v)//2]
        v2 = v[len(v)//2:]
        selector = root.new_var()
        self.add_subproblem(HeuleEncoding(root, *v1, +selector))
        self.add_subproblem(HeuleEncoding(root, *v2, -selector))


AtMostOne = HeuleEncoding


class ExactlyOne(SatFormula):
    def __init__(self, root: SatProblem, *v):
        super().__init__()
        self.add_subproblem(AtLeastOne(root, *v))
        self.add_subproblem(AtMostOne(root, *v))
