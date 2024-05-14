from sudoku import parse_sudoku, pretty_print, initialise_constraints,valid_sudoku, fitness, open_fields, available_values
import numpy as np

sudoku = parse_sudoku("sudoku1.txt") # This should not be modified, but you should make deep copies when making children
constraints = initialise_constraints(sudoku) # You should not need to modify this
pretty_print(sudoku)
print(open_fields(sudoku))
print(available_values(sudoku))
