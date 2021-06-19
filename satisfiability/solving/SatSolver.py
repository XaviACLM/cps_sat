from __future__ import annotations
import multiprocessing

from satisfiability.modeling.problem import SatProblem
from satisfiability.solving.Result import Result


class SatSolver:
    def solve(self, problem: SatProblem, timeout=None) -> Result:
        if timeout is None:
            return self._solve(problem)
        result = multiprocessing.Queue()
        thread = multiprocessing.Process(target=self._solve_helper, args=(problem, result))
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            thread.kill()
            thread.join()
            return Result.timed_out()
        return result.get()

    def _solve_helper(self, problem: SatProblem, result):
        result.put(self._solve(problem))

    def _solve(self, problem: SatProblem) -> Result:
        raise NotImplementedError()


