from sudoku import parse_sudoku, pretty_print, initialise_constraints,valid_sudoku, fitness, open_fields, available_values
import numpy as np

sudoku = parse_sudoku("sudoku1.txt")
constraints = initialise_constraints(sudoku)
pretty_print(sudoku)
print(available_values(sudoku))
