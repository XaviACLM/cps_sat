**cps-sat** is a small constraint modeling library built around Boolean formulae in conjunctive normal form (CNF), designed for use with external SAT solvers such as [Kissat](https://github.com/arminbiere/kissat). It provides a Python interface for constructing problems compositionally - from basic propositional atoms to reification, cardinality, and others.

This project originated as part of the Combinatorial Problem Solving course at UPC’s Master in Innovation and Research in Informatics. The coursework portion, focusing on a particular modeled problem, is omitted from this repository. What remains is a general-purpose toolkit for CNF-based modeling, useful in SAT-flavored constraint programming projects.

### Structure

See [this report](CPS_MIRI___Boolean_Satisfiability_Project_Report__NLSP_removed_.pdf).

### Example Problem

An example use of the library is provided in `example.py`, located at the top level of the repository. This example models a variation of the classic queens problem: Given a square board of size *N*, a maximum budget *M*, and piece costs *Q*, *R*, and *B* (for queens, rooks, and bishops respectively), the script searches for a configuration of pieces that meets the following conditions:

- Every square on the board must be attacked by at least one piece.
- The total cost of all placed pieces must be less than *M*.
- Pieces can attack *through* one another (i.e., no blocking).

#### Modeling Strategy

- For each board square `(x, y)`, a Boolean variable `is_attacked[x][y]` indicates whether the square is covered. These are all constrained to be `True`.
- For each row, column, and diagonal, a separate variable (e.g. `is_row_attacked[x]`) encodes whether that entire line is attacked. A square being attacked implies that at least one of its row, column, or diagonal lines must be marked as attacked.
- For each square, four variables represent whether it contains a piece that attacks along a particular direction (horizontal, vertical, positive diagonal, or negative diagonal). These link the "line-level" variables to actual piece placements.
- Each square also carries three Boolean variables indicating whether it contains a rook, bishop, or queen. These determine which kinds of directional attackers can exist in that cell. For example, `is_row_attacker[x][y]` implies that the piece there must be a rook or queen.
- Additional constraints ensure:
  - No square contains more than one piece.
  - The total cost of all placed pieces (weighted according to their type) stays below the given budget.

Although some directional-attacker variables could be omitted (since e.g. all row attackers are also column atackers), they are retained here for clarity and extensibility.
