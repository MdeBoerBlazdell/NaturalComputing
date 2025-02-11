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
                                               max_generations=max_gens, 
                                               mutation_rate=m,
                                               nr_children=c,
                                               k_select=k)
        gens.append(iterations)
    return gens

# Fitness weighed selection (edit sudoku_evolution.evolve_sudoku accordingly)
for s in range(5,9):
    for m in [0.01, 0.05, 0.1]:
        k = 0 
        sudoku_string = f"./project/sudokus/sudoku3_{s}v.txt"
        sudoku = parse_sudoku(sudoku_string)
        gens = solving_experiment(12, sudoku, 10000, m, 10, k)
        print(f"fw_m{m}_v{s}_p3 = {gens}")
        print(f"fw_m{m}_v{s}_p3.sort()")
        print(f"fw_m{m}_v{s}_p3 = fw_m{m}_v{s}_p3[1:-1]")
        print()

# Tournament selection (edit sudoku_evolution.evolve_sudoku accordingly)
#for s in range(5,9):
#    for k in range(2,11):
#        for m in [0.01, 0.05, 0.1]:
#            sudoku_string = f"./project/sudokus/sudoku3_{s}v.txt"
#            sudoku = parse_sudoku(sudoku_string)
#            gens = solving_experiment(12, sudoku, 10000, m, 10, k)
#            print(f"k{k}_m{m}_v{s}_p3 = {gens}")
#            print(f"k{k}_m{m}_v{s}_p3.sort()")
#            print(f"k{k}_m{m}_v{s}_p3 = k{k}_m{m}_v{s}_p3[1:-1]")
#            print()