from sudoku import parse_sudoku, pretty_print, initialise_constraints,valid_sudoku, fitness, open_fields, available_values
import numpy as np
import random

# Hyperparameters of the evolutionary algorithm
MUTATION_RATE = 1 # Test value while crossover is not implemented, TODO change to suitable value later
CROSSOVER_RATE = 1
NUM_CHILDREN = 10
MAX_GENERATIONS = 10000

def solve_sudoku(sudoku):
    solved = False
    gens = 0

    # The original sudoku is the first parent
    parents = [sudoku.copy()]
    while(not solved and gens < MAX_GENERATIONS):
        children = generate_children(sudoku, parents)
        print(f"Generation {gens} has generated {len(children)} children")
        fitness_scores = []

        for c in children:
            # Check whether any child is the solved sudoku
            if(valid_sudoku(c)):
                return (True, c, gens)
            # Compute and store fitness of children
            fitness_scores.append((c,fitness(c)))

        total_fitness = np.sum(f for c,f in fitness_scores)

        # Sample parents to seed the next generation
        new_parents = []

        for c, f in fitness_scores:
            if random.random() <= (f/(total_fitness-f)):
                new_parents.append(c)
        
        # Failsafe: if no parents get sampled, sample parent with highest fitness
        if len(new_parents) == 0:
            new_parents.append(max(fitness_scores, key = lambda x:x[1])[0])

        parents = new_parents
        print(f"Generation {gens} sampled {len(parents)} new parents")
        gens += 1
    return (False, sudoku, gens)


def generate_children(sudoku,parents):
    children = []

    # Store which fields we are free to manipulate without changing
    # the original sudoku
    positions = open_fields(sudoku)

    #for p in range(len(parents)):
    while(len(children) < NUM_CHILDREN): 
        p = random.choice(parents)
        child = p.copy()

        # Make sure the child is a complete sudoku
        vals = available_values(child)
        if not len(vals) == 0:
            for i,j in positions:
                if child[i][j] == 0:
                    val = random.choice(vals)
                    child[i][j] = val
                    vals.remove(val)

        if random.random() <= CROSSOVER_RATE:        
            # TODO: Implement crossover between parents
            place_holder = 1

        if random.random()<= MUTATION_RATE:
            # Mutation: swap two digits in the sudoku puzzle
            i1,j1 = random.choice(positions)
            i2,j2 = random.choice(positions)
            temp = child[i1][j1]
            child[i1][j1] = child[i2][j2]
            child[i2][j2] = temp
        children.append(child)    
        
    return children