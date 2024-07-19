from sudoku import parse_sudoku, pretty_print
from sudoku_evolution import evolve_solution
import matplotlib.pyplot as plt

# iterations, solution = evolve_solution(sudoku)
# if iterations == 9_999:
#     print("No solution found after 10.000 generations")
#     plt.plot(solution)
#     plt.savefig("results.png")
# if iterations < 9_999:    
#     print(f"Solved after {iterations} generations")
#     pretty_print(solution)

def solving_experiment(trials, sudoku, max_gens, m, c, k):
    gens = []
    for i in range(trials):
        iterations, solution = evolve_solution(sudoku=sudoku, 
                                               MAX_GENERATIONS=max_gens, 
                                               MUTATION_RATE=m,
                                               NR_CHILDREN=c,
                                               K_SELECT=k)
        gens.append(iterations)
    print(gens)

sudoku = parse_sudoku("sudokus/sudoku1_5v.txt")
solving_experiment(12, sudoku, 10000, 0.01, 10, 2)