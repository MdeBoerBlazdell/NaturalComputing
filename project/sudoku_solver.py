from sudoku import parse_sudoku, pretty_print
from sudoku_evolution import evolve_solution
import matplotlib.pyplot as plt

sudoku = parse_sudoku("./project/sudoku1_8v.txt")
iterations, solution = evolve_solution(sudoku)
if iterations == 9_999:
    plt.plot(solution)
    plt.savefig("./project/results.png")
if iterations < 9_999:    
    print(f"Solved after {iterations} generations")
    pretty_print(solution)
