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

for s in [5,6,7,8]:
    sudoku_string = f"./project/sudokus/sudoku2_{s}v.txt"
    sudoku = parse_sudoku(sudoku_string)
    for k in [2,3,4,5,6,7,8,9,10]:
        for m in [0.01, 0.05, 0.1]:
            print(f"Gens of {s}v, k={k}, m={m}:")
            solving_experiment(12, sudoku, 10000, m, 10, k)