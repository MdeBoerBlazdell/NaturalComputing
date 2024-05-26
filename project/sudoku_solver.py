from sudoku import parse_sudoku, pretty_print
from sudoku_evolution import evolve_solution, crossover
import numpy as np

sudoku = parse_sudoku("./project/sudoku1_5v.txt")
# constraints = initialise_constraints(sudoku) # You should not need to modify this
# found, solution, gens = solve_sudoku(sudoku)
# if(found):
#     print(f"Solution found after {gens} generations! \n Solution: ")
#     pretty_print(solution)
# else:
#     print(f"No solution found after {gens} generations")
iterations, solution = evolve_solution(sudoku)
print(f"Solved after {iterations} generations")
pretty_print(solution)
