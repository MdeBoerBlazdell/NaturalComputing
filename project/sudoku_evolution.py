from sudoku import (
    valid_sudoku,
    fitness_from_sudoku,
    fitness_from_values,
    determine_open_fields,
    available_values,
    is_solution,
    fill_in_sudoku,
)
import numpy as np
import random

# Hyperparameters of the evolutionary algorithm
MUTATION_RATE = 0.01  # Test value while crossover is not implemented, TODO change to suitable value later
NUM_CHILDREN = 10
MAX_GENERATIONS = 10000

'''
def solve_sudoku(sudoku):
    solved = False
    gens = 0

    # The original sudoku is the first parent
    parents = [sudoku.copy()]
    while not solved and gens < MAX_GENERATIONS:
        children = generate_children(sudoku, parents)
        print(f"Generation {gens} has generated {len(children)} children")
        fitness_scores = []

        for c in children:
            # Check whether any child is the solved sudoku
            if valid_sudoku(c):
                return (True, c, gens)
            # Compute and store fitness of children
            fitness_scores.append((c, fitness_from_sudoku(c)))

        total_fitness = np.sum(f for c, f in fitness_scores)

        # Sample parents to seed the next generation
        new_parents = []

        for c, f in fitness_scores:
            if random.random() <= (f / (total_fitness - f)):
                new_parents.append(c)

        # Failsafe: if no parents get sampled, sample parent with highest fitness
        if len(new_parents) == 0:
            new_parents.append(max(fitness_scores, key=lambda x: x[1])[0])

        parents = new_parents
        print(f"Generation {gens} sampled {len(parents)} new parents")
        gens += 1
    return (False, sudoku, gens)

def generate_children(sudoku, parents):
    children = []

    # Store which fields we are free to manipulate without changing
    # the original sudoku
    positions = determine_open_fields(sudoku)

    # for p in range(len(parents)):
    while len(children) < NUM_CHILDREN:
        p = random.choice(parents)
        child = p.copy()

        # Make sure the child is a complete sudoku
        vals = available_values(child)
        if not len(vals) == 0:
            for i, j in positions:
                if child[i][j] == 0:
                    val = random.choice(vals)
                    child[i][j] = val
                    vals.remove(val)

        # if random.random() <= CROSSOVER_RATE:
            # TODO: Implement crossover between parents
            # place_holder = 1

        if random.random() <= MUTATION_RATE:
            # Mutation: swap two digits in the sudoku puzzle
            i1, j1 = random.choice(positions)
            i2, j2 = random.choice(positions)
            temp = child[i1][j1]
            child[i1][j1] = child[i2][j2]
            child[i2][j2] = temp
        children.append(child)

    return children
'''

def evolve_solution(
    sudoku,
    MAX_GENERATIONS=MAX_GENERATIONS,
    MUTATION_RATE=MUTATION_RATE,
    NR_CHILDREN=NUM_CHILDREN,
):
    values = available_values(sudoku)
    open_fields = determine_open_fields(sudoku)
    best_fitness = fitness_from_sudoku(sudoku)
    best_fitness_per_generation = []
    # The solution is a permutation of the values list, where each element in values is filled in in the open_fields with the same index

    # Start with an initial set of parents, derived from the original sudoku configuration
    previous_generation = []
    for _ in range(0, NR_CHILDREN):
        vals = random.sample(values, len(values))
        previous_generation.append(vals)

    for generation in range(0, MAX_GENERATIONS):
        best_in_gen = max([fitness_from_values(sudoku, open_fields, c) for c in previous_generation])
        best_fitness_per_generation.append(best_in_gen)

        print(f"{generation} : {best_fitness}")
        cum_fitness = np.sum(
            [fitness_from_values(sudoku, open_fields, c) for c in previous_generation]
        )
        weights = [
            fitness_from_values(sudoku, open_fields, c) / cum_fitness for c in previous_generation
        ]

        new_children = []
        for _ in range(0, NR_CHILDREN // 2):
            # for each child, we generate two parents from the previous generation

            parents = random.choices(previous_generation, weights=weights, k=2)

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
