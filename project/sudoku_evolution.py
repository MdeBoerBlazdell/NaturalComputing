from sudoku import (
    valid_sudoku,
    fitness_from_sudoku,
    local_fitness_from_sudoku,
    local_fitness_from_values,
    fitness_from_values,
    determine_open_fields,
    available_values,
    is_solution,
    fill_in_sudoku,
)
import numpy as np
import random
import heapq

# Hyperparameters of the evolutionary algorithm
# TODO Experiment with full range of K_SELECT as well as MUTATION_RATE (or at least justify choices)
MUTATION_RATE = 0.01
K_SELECT = 7
NUM_CHILDREN = 10
MAX_GENERATIONS = 10000

def evolve_solution(
    sudoku,
    MAX_GENERATIONS=MAX_GENERATIONS,
    MUTATION_RATE=MUTATION_RATE,
    NR_CHILDREN=NUM_CHILDREN,
    K_SELECT = K_SELECT
):
    values = available_values(sudoku)
    open_fields = determine_open_fields(sudoku)
    best_fitness = local_fitness_from_sudoku(sudoku, open_fields)
    best_fitness_per_generation = []
    # The solution is a permutation of the values list, where each element in values is filled in in the open_fields with the same index

    # Start with an initial set of parents, derived from the original sudoku configuration
    previous_generation = []
    for _ in range(0, NR_CHILDREN):
        vals = random.sample(values, len(values))
        previous_generation.append(vals)

    for generation in range(0, MAX_GENERATIONS):
        # For testing purposes and to generate result: store highest found fitness over all past generations
        best_in_gen = max([local_fitness_from_values(sudoku, open_fields, c) for c in previous_generation])
        best_fitness_per_generation.append(best_in_gen)

        print(f"{generation} : {best_in_gen}")
        #cum_fitness = np.sum(
        #    [local_fitness_from_values(sudoku, open_fields, c) for c in previous_generation]
        #    )
        #weights = [
        #     local_fitness_from_values(sudoku, open_fields, c) / cum_fitness for c in previous_generation
        #    ]

        new_children = []
        for _ in range(0, NR_CHILDREN // 2):
            # Fitness-weighed selection
            # parents = np.random.choice(previous_generation, size = 2, replace = False, p = weights)

            # Tournament selection
            parent_pool = random.sample(previous_generation, k=K_SELECT)
            parent_pool_fitness = [(p, local_fitness_from_values(sudoku, open_fields, p)) for p in parent_pool]
            sorted_pool = sorted(parent_pool_fitness, key = lambda p: p[1])[::-1]
            parents = [p[0] for p in sorted_pool][:2]

            child1, child2 = crossover(parents)
            # For both children, we mutate with a probability of MUTATION_RATE
            if random.random() < MUTATION_RATE:
                child1 = mutate(child1)
            if random.random() < MUTATION_RATE:
                child2 = mutate(child2)
            new_children.append(child1)
            new_children.append(child2)


        for c in new_children:
            if is_solution(sudoku, open_fields, c):
                return generation, fill_in_sudoku(sudoku, open_fields, c)
        previous_generation = new_children
        best_fitness_per_generation.append(best_fitness)

    print(f"No solution found after {MAX_GENERATIONS} generations")
    return generation, best_fitness_per_generation

def crossover(parents):
    """
    Creates two new children based on a pair of parents while ensuring that children are valid
    (i.e. same distribution of values as their parents)
    """
    parent1, parent2 = parents
    partition_size = len(parent1) // 3

    child1, child2 = (
        parent1[partition_size:-partition_size],
        parent2[partition_size:-partition_size],
    )

    parent1 = [x for x in parent1 if x not in child2]
    parent2 = [x for x in parent2 if x not in child1]

    child1 = parent2[-partition_size:] + child1 + parent2[:partition_size]
    child2 = parent1[-partition_size:] + child2 + parent1[:partition_size]

    return child1, child2


def mutate(values):
    """
    Randomly swap the value at two indices in the values list
    """
    indices = random.choices(range(len(values)), k=2)
    temp = values[indices[0]]
    values[indices[0]] = values[indices[1]]
    values[indices[1]] = temp
    return values
