from random import random, sample,choice, choices, randrange
from string import ascii_letters

target_string = "ABCDEFghijklmn"
l = len(target_string)
N = 200  # Population size
mu = 1 / l  # Mutation rate
pc = 1  # cross-over probability
K = 2  # number of randomly selected individuals
alphabet = ascii_letters


def fitness(s: str) -> int:
    """
    Calculate how many characters correspond to a character in the target_string
    Must be an exact match in location and character
    """
    matches = 0
    for i in range(0, len(s)):
        if s[i] == target_string[i]:
            matches += 1
    return matches


def crossover(parent1: str, parent2: str) -> tuple[str, str]:
    """
    We generate two new children from the parents. We do this by:
    Take the first and last 2 elements from the parents.
    The last 2 elements from parent1 become the first 2 elements from child2
    And vice versa. The first 2 elements become the last 2 elements from child2 
    and vice versa. The middle elements from parent1 become the middle elements from child1
    and the same for the other parent
    """
    middle1, middle2 = parent1[2:-2], parent2[2:-2]
    complement1 = [s for s in parent2 if s not in middle1]
    complement2 = [s for s in parent1 if s not in middle2]
    child1 = (
        "".join(complement1[-2:]) + middle1 + "".join(complement1[:2])
    )
    child2 = (
        "".join(complement2[-2:]) + middle2 + "".join(complement2[:2])
    )
    return child1, child2

def mutate(s:str, mu:float =0.07) -> str:
    """
    With a mutation rate of mu, swap two random elements in the string with each other
    """
    if random() < mu:
        elem1 = randrange(len(s))
        elem2 = randrange(len(s))
        l = list(s)
        l[elem1] = s[elem2]
        l[elem2] = s[elem1]
        return "".join(l)
    return s
        

def generate_children(population: list[str], mu,K, N):
    """
    Generate a new population of size N from a given population.
    In each iteration:
    - select K possible parents
    - sort K parents on fitness score
    - create children with highest 2 fitness scores
    - mutate children with mutation rate mu
    return new population of children
    """
    children = []
    for i in range(0, N // 2):
        parents = sample(population, K)
        parents = sorted(parents, key=fitness,reverse=True)[0:2]
        child1, child2 = crossover(parents[0], parents[1])
        child1, child2 = mutate(child1,mu), mutate(child2,mu)
        children.append(child1)
        children.append(child2)
    return children

def tournament_selection(
    K: int, target: str, alphabet: str, mu: float, N: int, gmax: int = 100
) -> str:
    population = [choices(alphabet,k=len(target)) for _ in range(0, N)]
    population = list(map(lambda x: "".join(x), population))
    
    for generation in range(0,gmax):
        for p in population:
            if fitness(p) == len(target): # we have found a solution
                return p, generation
        population = generate_children(population, (1/len(target)), K,N)
    print(population)
    return "FAILED"

print(tournament_selection(K, target_string, alphabet, mu=1.0, N=200, gmax=100))
