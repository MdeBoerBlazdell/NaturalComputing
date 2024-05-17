from sudoku import parse_sudoku, pretty_print, initialise_constraints,valid_sudoku, fitness, open_fields, available_values
from sudoku_evolution import solve_sudoku
import numpy as np

sudoku = parse_sudoku("project/sudoku_5v.txt") # This should not be modified, but you should make deep copies when making children
# constraints = initialise_constraints(sudoku) # You should not need to modify this
solution, gens = solve_sudoku(sudoku)
print(f"Solution found after {gens} generations! \n Solution: ")
pretty_print(solution)
