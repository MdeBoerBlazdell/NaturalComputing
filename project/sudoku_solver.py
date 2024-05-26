from sudoku import parse_sudoku, pretty_print
from sudoku_evolution import evolve_solution
import matplotlib.pyplot as plt

sudoku = parse_sudoku("sudoku_test.txt")
# constraints = initialise_constraints(sudoku) # You should not need to modify this
# found, solution, gens = solve_sudoku(sudoku)
# if(found):
#     print(f"Solution found after {gens} generations! \n Solution: ")
#     pretty_print(solution)
# else:
#     print(f"No solution found after {gens} generations")
iterations, solution = evolve_solution(sudoku)
if iterations == 9_999:
    plt.plot(solution)
    plt.savefig("results.png")
if iterations < 9_999:    
    print(f"Solved after {iterations} generations")
    pretty_print(solution)
