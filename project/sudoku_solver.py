from sudoku import parse_sudoku, pretty_print
from sudoku_evolution import evolve_solution
import matplotlib.pyplot as plt
from timeit import default_timer as timer
import pandas as pd

MUTATION_RATE = 0.1
K_SELECT = [5,6,7,8]
MAX_GENERATIONS = 10_000
NR_CHILDREN = 10

results = {}

def run_trial(sudoku, k, max_gens = MAX_GENERATIONS, mutation_rate = MUTATION_RATE, nr_children=NR_CHILDREN):
    start = timer()
    iterations, _ = evolve_solution(sudoku=sudoku, max_generations=max_gens, mutation_rate=mutation_rate, nr_children=nr_children, k_select=k)
    end = timer()
    elapsed_time = end - start # in seconds
    return iterations, elapsed_time

for s in range(1,4):
    for k in K_SELECT:
        res = []
        sudoku_string = f"inputs/sudoku{s}_{k}v.txt"
        sudoku = parse_sudoku(sudoku_string)

        for _ in range(0,5): # run experiment 5 times
            it, time = run_trial(sudoku, k)
            res.append((it, time))
            results[(s,k)] = res

results = pd.DataFrame(results.items(), columns=['Hyper-parameters', 'Iterations, time (s)'])    
results.to_csv('results.csv', index=False)        


