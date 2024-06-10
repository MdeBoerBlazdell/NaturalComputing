from sudoku import parse_sudoku, pretty_print
from sudoku_evolution import evolve_solution
import matplotlib.pyplot as plt

sudoku = parse_sudoku("sudokus/sudoku1_8v.txt")
iterations, solution = evolve_solution(sudoku)
if iterations == 9_999:
    print("No solution found after 10.000 generations")
    plt.plot(solution)
    plt.savefig("results.png")
if iterations < 9_999:    
    print(f"Solved after {iterations} generations")
    pretty_print(solution)