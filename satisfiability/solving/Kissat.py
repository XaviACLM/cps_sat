import subprocess
import tempfile

from satisfiability.config import KISSAT_PATH
from satisfiability.modeling.problem import SatProblem
from satisfiability.solving.Result import Result
from satisfiability.solving.SatSolver import SatSolver


class Kissat(SatSolver):
    def _solve(self, problem: SatProblem) -> Result:
        with tempfile.NamedTemporaryFile(mode="wt") as f:
            problem.write_to(f)
            f.seek(0)
            command = [KISSAT_PATH, "-q", f.name]
            s = subprocess.run(" ".join(command), shell=True, stdout=subprocess.PIPE)
            output = s.stdout.decode("utf-8")

        lines = iter(output.splitlines())
        line = next(lines)
        while not line.startswith("s"):
            line = next(lines)
        if line[2:] == "UNSATISFIABLE":
            return Result.unsatisfiable()
        elif line[2:] != "SATISFIABLE":
            raise Exception("Unknown format for kissat result")

        mapvar = list(problem.vars)
        assignments = {}

        def get_line():
            try:
                return next(lines)
            except StopIteration:
                return None

        line = get_line()
        while line is not None:
            if line.startswith("v"):
                for item in line.split():
                    if item in ["v", "0"]:
                        continue
                    if item.startswith("-"):
                        truthiness = False
                        index = int(item[1:])
                    else:
                        truthiness = True
                        index = int(item)
                    assignments[index] = truthiness
            line = get_line()
        if len(assignments) != len(mapvar):
            raise Exception("Kissat result did not assign all variables")
        return Result.satisfiable(assignments)
