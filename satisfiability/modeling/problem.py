from __future__ import annotations

from satisfiability.modeling.primitives import Variable
from satisfiability.solving.Result import Result


class SatFormula:
    def __init__(self):
        self.local_clauses = []
        self.subformulae = []

    def add_clause(self, *new_clause):
        if type(new_clause[0]) in (list, tuple):
            raise TypeError("SatProblem.add_clause does not take a single argument")
        self.local_clauses.append(new_clause)

    def add_subproblem(self, subformula: SatFormula):
        self.subformulae.append(subformula)

    @property
    def clauses(self):
        for clause in self.local_clauses:
            yield clause
        for subformula in self.subformulae:
            for clause in subformula.clauses:
                yield clause

    @property
    def qt_clauses(self):
        return len(self.local_clauses) + sum((subformula.qt_clauses for subformula in self.subformulae))


class SatProblem(SatFormula):
    def __init__(self):
        super().__init__()

        self.names = dict()

        self._var_creation_counter = 0

    @property
    def qt_vars(self):
        return self._var_creation_counter

    @property
    def vars(self):
        for v in range(1, self.qt_vars+1):
            yield Variable(v)

    def new_var(self, name=None):
        self._var_creation_counter += 1
        v = self._var_creation_counter
        self.names[v] = name
        return Variable(v)

    def write_to(self, filestream):
        filestream.write("p cnf {} {}\n".format(self.qt_vars, self.qt_clauses))
        for clause in self.clauses:
            filestream.write(" ".join(map(str, clause)))
            filestream.write(" 0\n")

    def report_result(self, result: Result, only_named_vars=True):
        if not result.is_satisfiable:
            print("Unsatisfiable")
            return
        print("Satisfiable:")
        for var in self.vars:
            if self.names[var] is not None:
                print(self.names[var], result[var])
            elif not only_named_vars:
                print(var, result[var])
