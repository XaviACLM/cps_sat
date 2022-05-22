# cps_sat

This is part of a project turned in to the Combinatorial Problem Solving course of the Master in Innovation and Research in Engineering, at Universitat Politècnica de Catalunya. Obviously, part of the original project is absent from this repository - namely, the part that actually models and solves the problem presented in class.

The remainder is a small but fairly versatile library, serving to model boolean formulae in conjunctive normal form, and solve them by interfacing with (a previously existing installation of) Kissat. Details on the capabilities and implementation of each part of the module can be found in the first part of the project report, available as a pdf in the top level directory.

### Example code

An example for how to use the library is provided, in example.py, at the top-level directory. This is for a problem loosely related to the well-known queens problem. For a given (square) board size, positive integer costs R, B, Q (for rook, queens, and bishops), and maximum cost M, the script finds (or verifies the nonexistence of) an arrangement of rooks, queens and bishops that attacking each square on the board (assuming that they can attack through each other), such that their total cost (according to R, B, Q) is less than M.

A brief explanation of how this works: For each square on the chessboard we have a variable (is_attacked[x][y]) modelling whether that square is attacked. All these variables are constrained to be true.

For each row, column, and positive/negative diagonal, we have a variable, we have a variable (is_row_attacked[x], etc), that models whether that entire row/etc is attacked by a single piece - in the column case, for instance, this would be true if that column contained a rook or queen. We add the constraint that, if a cell is attacked, then either the row, column, or positive/negative diagonal that it belongs to must be attacked.

For each cell, we add four variables, corresponding whether in that cell there is a piece that attacks horizontally, vertically, along the positive diagonal, or along the negative diagonal. We add the constraint that, if a row/etc is attacked, then one of its cells contains the relevant type of attacker.

We add for each cell three variables, describing whether it is a rook, bishop, or queen, and add the reasonable constraints relating to the variables from the last paragraph - e.g. is_row_attacker[x][y] => is_rook[x][y] or is_queen[x][y]. Finally, we add the constraint that no cell can contain more than one piece at once, and the relevant cardinality constraints.



Note that, since our pieces either attack along the rows/columns, along the diagonals, or both, we could've cut half the variables relating to whether a certain cell contains a certain type of attacker. Nonetheless, this was avoided, both for clarity and also because it would allow easy generalization if necessary.
