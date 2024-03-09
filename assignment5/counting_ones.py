from random import random
from bitarray import bitarray
import matplotlib.pyplot as plt 
import numpy as np

# Setting of hyper parameters that will be used throughout the script
l = 100 # length of target string
mu = 1/l # mutation rate
generations = 1500 # number of generations we generate, used to constrain the runtime
bit_string = bitarray(l)

def initialise_bitstring(l):
    """
    Makes a random bitstring of length l
    """
    bit_string = bitarray(l)
    for i in range(0,l):
        if random() > 0.50:
            bit_string[i] ^= 1
    return bit_string


def calculate_fitness(arr):
    """
    Calculates the sum of a bitarray, i.e. max(arr) == len(arr)
    """
    return sum(arr)

def mutate(arr, mu=0.01):
    """
    For each bit in the array, flip the bit with a probability of mu. 
    Returns a copy of the bitarray that is possibly mutated.
    """
    bits = arr.copy()
    for i in range(0,len(bits)):
        if random() < mu:
            bits[i] ^= 1 # We make use of the array consisting of only bits and do an XOR to flip the bit
    return bits

def question1(bit_string, generations=1500, mu=0.01):
    """
    Code for question 5.2.1. 
    We start with a randomly initialised bit_string. For each generation, we do the following:
    1. compute the fitness. If it is higher than the current highest found fitness, update the highest found fitness
    2. mutate the bitstring with a probability mu. 
    3. if fitness(mutated string) > fitness(previous string), then update the global bit_string
    """
    best_fitness = np.zeros(generations) # keep track of the best found fitness per generation
    current_best_fitness = 0
    for i in range(0,generations):
        fitness = calculate_fitness(bit_string)
        if fitness == len(bit_string):
            best_fitness[i:] = len(bit_string)
            return best_fitness
        if fitness > current_best_fitness: # conditionally update best_fitness if we find a new optimum
            current_best_fitness = fitness
            best_fitness[i] = fitness
        else:
            best_fitness[i] = fitness
        xm = mutate(bit_string)
        if calculate_fitness(xm) > fitness: # conditionally update bit_string if we have found a better string
            bit_string = xm
    return best_fitness
    
def question2(bit_string, generations=1500, mu=0.01):
    """
    Code for question 5.2.2. 
    We start with a randomly initialised bit_string. For each generation, we do the following:
    1. compute the fitness. If it is higher than the current highest found fitness, update the highest found fitness
    2. mutate the bitstring with a probability mu. 
    3. Set the global bit_string to the mutated bitstring
    """
    best_fitness = np.zeros(generations)
    current_best_fitness = 0
    for i in range(0,generations):
        fitness = calculate_fitness(bit_string)
        if fitness == len(bit_string):
            best_fitness[i:] = len(bit_string)
            return best_fitness
        if fitness > current_best_fitness:
            current_best_fitness = fitness
            best_fitness[i] = fitness
        else:
            best_fitness[i] = current_best_fitness
        xm = mutate(bit_string)
        bit_string = xm
    return best_fitness
    
fitnesses1 = question1(initialise_bitstring(l), generations, mu)
fitnesses2 = question2(initialise_bitstring(l), generations, mu)

plt.figure()
plt.plot(fitnesses1, label="Only replace when improved")
plt.plot(fitnesses2, label="Always replace")
plt.title("Counting ones problem")
plt.xlabel("Generations")
plt.ylabel("Fitness (sum of bits)")
plt.legend()
plt.savefig("1 trial.png")

def question4(generation=1500, mu=0.01, nr_trials=1000):
    """
    Here, we repeat question 1 and 2, but this time we take the average over nr_trials for both.
    This is to prevent stochastic operations from influencing the final results too much
    """
    avg_fitness1 = np.zeros(1500)
    avg_fitness2 = np.zeros(1500)
    for i in range(0,nr_trials):
        avg_fitness1 = avg_fitness1 + question1(initialise_bitstring(l), generations, mu)
        avg_fitness2 = avg_fitness2 + question2(initialise_bitstring(l), generations, mu)
    avg_fitness1 = avg_fitness1 / nr_trials
    avg_fitness2 = avg_fitness2 / nr_trials
    return (avg_fitness1, avg_fitness2)

avg_fitness1, avg_fitness2 = question4(generations, mu)
plt.figure()
plt.plot(avg_fitness1, label="Only replace when improved")
plt.plot(avg_fitness2, label="Always replace")
plt.title("Counting ones problem averaged over 1000 runs")
plt.xlabel("Generations")
plt.ylabel("Fitness (sum of bits)")
plt.legend()
plt.savefig("average_1000trials.png")
