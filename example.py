from itertools import chain, product, repeat

from satisfiability.modeling.problem import SatProblem, SatFormula
from satisfiability.modeling.reification import PartiallyReified
from satisfiability.modeling.subproblems.binary_relations import Implies
from satisfiability.modeling.subproblems.cardinality.unary import AtMostOne
from satisfiability.modeling.subproblems.cardinality.weighted import WeightedAtMost
from satisfiability.modeling.subproblems.shorthand import AllOf
from satisfiability.solving.Kissat import Kissat
from satisfiability.solving.Result import Result


class BoardProblem(SatProblem):
    """
    CNF formula modeling whether it is possible to attack an entire nxn board (n being the init arg board_size)
    using A queens, B rooks, and C bishops, such that A*queen_cost + B*rook_cost + C*bishop_cost <= max_cost
    """
    def __init__(self, board_size, max_cost, queen_cost, rook_cost, bishop_cost):
        super().__init__()
        self.board_size = board_size
        self.queen_cost = queen_cost
        self.rook_cost = rook_cost
        self.bishop_cost = bishop_cost

        is_attacked = [[self.new_var(name="is_attacked[{},{}]".format(x, y))
                        for x in range(board_size)]
                       for y in range(board_size)]
        self.add_subproblem(AllOf(self, *chain(*is_attacked)))

        is_row_attacked = [self.new_var(name="is_row_attacked[{}]".format(y)) for y in range(board_size)]
        is_column_attacked = [self.new_var(name="is_column_attacked[{}]".format(x)) for x in range(board_size)]
        is_posdiag_attacked = [self.new_var(name="is_row_attacked[{}]".format(s)) for s in range(2*board_size-1)]
        is_negdiag_attacked = [self.new_var(name="is_column_attacked[{}]".format(d if d<board_size
                                                                                 else d-2*board_size+1)
                                            ) for d in range(2*board_size-1)]

        # a square being attacked means that square's row/column/etc is attacked
        for x, y in product(range(board_size), repeat=2):
            local_attack = SatFormula()
            local_attack.add_clause(is_row_attacked[x],
                                    is_column_attacked[y],
                                    is_posdiag_attacked[x+y],
                                    is_negdiag_attacked[x-y])
            self.add_subproblem(PartiallyReified(is_attacked[x][y], local_attack))

        is_row_attacker = [[self.new_var(name="is_row_attacker[{},{}]".format(x, y))
                            for x in range(board_size)]
                           for y in range(board_size)]
        is_column_attacker = [[self.new_var(name="is_column_attacker[{},{}]".format(x, y))
                               for x in range(board_size)]
                              for y in range(board_size)]
        is_posdiag_attacker = [[self.new_var(name="is_posdiag_attacker[{},{}]".format(x, y))
                                for x in range(board_size)]
                               for y in range(board_size)]
        is_negdiag_attacker = [[self.new_var(name="is_negdiag_attacker[{},{}]".format(x, y))
                                for x in range(board_size)]
                               for y in range(board_size)]

        # a row/column/etc being attacked means there is a row/column/etc attacker in that row/column/etc
        for x in range(board_size):
            local_column_attack = SatFormula()
            local_column_attack.add_clause(*[is_column_attacker[x][y] for y in range(board_size)])
            self.add_subproblem(PartiallyReified(is_column_attacked[x], local_column_attack))
        for y in range(board_size):
            local_row_attack = SatFormula()
            local_row_attack.add_clause(*[is_row_attacker[x][y] for x in range(board_size)])
            self.add_subproblem(PartiallyReified(is_row_attacked[y], local_row_attack))
        for s in range(2*board_size-1):
            local_posdiag_attack = SatFormula()
            local_posdiag_attack.add_clause(*[is_posdiag_attacker[x][s-x] for x in range(max(0,s-board_size+1),
                                                                                         min(board_size,s+1))])
            self.add_subproblem(PartiallyReified(is_posdiag_attacked[s], local_posdiag_attack))
        for d in range(-board_size+1, board_size):
            local_negdiag_attack = SatFormula()
            local_negdiag_attack.add_clause(*[is_negdiag_attacker[x][d+x] for x in range(max(0, -d),
                                                                                         board_size + min(0, -d))])
            self.add_subproblem(PartiallyReified(is_negdiag_attacked[d], local_negdiag_attack))

        is_queen = self.is_queen = [[self.new_var(name="is_queen[{},{}]".format(x, y))
                                     for x in range(board_size)] for y in range(board_size)]
        is_rook = self.is_rook =  [[self.new_var(name="is_rook[{},{}]".format(x, y))
                                    for x in range(board_size)] for y in range(board_size)]
        is_bishop = self.is_bishop = [[self.new_var(name="is_bishop[{},{}]".format(x, y))
                                       for x in range(board_size)] for y in range(board_size)]

        # row/column/etc attacker means there's a piece that attacks that row/column/etc
        for x, y in product(range(board_size), repeat=2):
            local_row_attacker = SatFormula()
            local_row_attacker.add_clause(is_rook[x][y], is_queen[x][y])
            self.add_subproblem(PartiallyReified(is_row_attacker[x][y], local_row_attacker))

            local_column_attacker = SatFormula()
            local_column_attacker.add_clause(is_rook[x][y], is_queen[x][y])
            self.add_subproblem(PartiallyReified(is_column_attacker[x][y], local_column_attacker))

            local_posdiag_attacker = SatFormula()
            local_posdiag_attacker.add_clause(is_bishop[x][y], is_queen[x][y])
            self.add_subproblem(PartiallyReified(is_posdiag_attacker[x][y], local_posdiag_attacker))

            local_negdiag_attacker = SatFormula()
            local_negdiag_attacker.add_clause(is_bishop[x][y], is_queen[x][y])
            self.add_subproblem(PartiallyReified(is_negdiag_attacker[x][y], local_negdiag_attacker))

        # only one of each thing in each place
        for x, y in product(range(board_size), repeat=2):
            self.add_subproblem(AtMostOne(self, is_queen[x][y], is_rook[x][y], is_bishop[x][y]))

        # cardinality constraint
        qt_squares = board_size*board_size
        self.add_subproblem(WeightedAtMost(self,
                                           chain(chain(*is_queen), chain(*is_rook), chain(*is_bishop)),
                                           chain(repeat(queen_cost, qt_squares),
                                                 repeat(rook_cost, qt_squares),
                                                 repeat(bishop_cost, qt_squares)),
                                           max_cost))

    def pretty_print(self, result: Result):
        if result.timed_out:
            print("TIMED OUT")
        if not result.satisfiable:
            print("UNSATISFIABLE")
        board_string = [["." for __ in range(self.board_size)] for _ in range(self.board_size)]
        for x, y in product(range(self.board_size), repeat=2):
            if result[self.is_rook[x][y]]:
                board_string[x][y] = "R"
            elif result[self.is_bishop[x][y]]:
                board_string[x][y] = "B"
            elif result[self.is_queen[x][y]]:
                board_string[x][y] = "Q"
        print("\n".join(["".join(line) for line in board_string]))


if __name__=="__main__":
    board_problem = BoardProblem(4, 4, 2, 1, 1)
    # with open("a.txt","w") as f:
    #     board_problem.write_to(f)
    solver = Kissat()
    result = solver.solve(board_problem, timeout=60)
    board_problem.report_result(result)
