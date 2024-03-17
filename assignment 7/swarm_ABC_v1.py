import os
import sys
import csv
from random import uniform, sample, choice
import numpy as np
from particle import Particle, extract_order_for_ABC, draw


import matplotlib.pyplot as plt
from celluloid import Camera
import warnings


# Set a new recursion limit
# Be cautious with the value; too high might cause a crash
sys.setrecursionlimit(10000)
warnings.simplefilter(action="ignore", category=RuntimeWarning)
project_dir = rf"."
n_dir_trial = len(os.listdir(os.path.join(project_dir, rf"trials")))
n_dir_data = len(os.listdir(os.path.join(project_dir, rf"data")))

w = 600
h = 600

test = False

"""
input : model M(X | θ), prior P(θ), population size N,
mutation covariance matrix Σ, thresholds
ε0 > . . . > εT
output : Sample θ1,T , . . . , θN,T
Draw θ0,1, . . . θ0,N from P(θ) accepting at ε0
j ← 1
foreach j ∈ 1, . . . , T do
k ← 1
while k < N do
Draw θ∗ uniformly from θ1, . . . , θN
Mutate θ∗ ← θ∗ + N(0, Σ)
if θ∗ is accepted at εj then
θk ,j ← θ∗ , k ← k + 1
end
end
end
"""


def generate_samples(n, threshold, target_alignment=1.0):
    """
    Initially we will have a uniform prior over alignment, coherence and separation
    of n elements. Samples must have |alignment - target_alignment| < threshold
    TODO: use order function for acceptance criteria
    """
    samples = np.zeros((n, 3))
    valid_samples = 0
    while valid_samples < n:
        sample = np.array([uniform(0,1), uniform(0,1), uniform(0,1)])
        avg_order = extract_order_for_ABC(run(15, sample[0],sample[1],sample[2]))
        if avg_order < threshold:
            samples[valid_samples,:] = sample
            valid_samples += 1
    return samples


def revised_ABC(population_size: int = 20):
    """
    This function goes over alignment, coherence and separation together.
    Other ABC function is only for coherence
    TODO: use order function for acceptance criteria. Already updated the step()
    function from the Particles to include parameters
    """

    thresholds = np.linspace(24, 1, population_size) + 0.1

    theta = np.zeros((20, population_size, 3))
    theta[0, :, :] = generate_samples(population_size, thresholds[0])
    print("generated all samples")
    for j in range(1, population_size):
        print(f"j = {j}")
        k = 1
        while k < population_size:
            new_sample = choice(theta[j - 1, :, :])
            # Because we reject all samples where the alignment > epsilon,
            # We update the new sample using this information, to prevent useless
            # creation and rejection of samples

            noise = np.array(
                [
                    uniform(-1, 1),
                    uniform(-1, 1),
                    uniform(-1, 1),
                ]
            )
            new_sample = new_sample + noise
            avg_order = extract_order_for_ABC(run(15, new_sample[0],new_sample[1],new_sample[2]))
            if avg_order < thresholds[j]:
                theta[j,k,:] = new_sample
                k += 1
    return theta


def run(n_steps,cohesion_strength=0.5,
        alignment_strength=0.02,
        separation_strength=0.1,  to_write=False, save_anim=False):

    with open(
        os.path.join(project_dir, rf"data\swarm_Motion_{n_dir_data}.txt"), "w"
    ) as file:

        data_for_ABC = []
        time_steps = n_steps
        N = 15

        if to_write:
            writer = csv.writer(file)
            writer.writerow([f"Particle_{i}, " for i in range(N)])

        swarm = [Particle(i) for i, _ in enumerate(range(0, N))]

        if save_anim:
            fig = plt.figure()
            camera = Camera(fig)

        for _ in range(0, time_steps):

            data = draw(swarm, cohesion_strength, alignment_strength, separation_strength)

            if to_write:
                writer.writerow(data)
            if save_anim:
                camera.snap()

            data_for_ABC.append(data)

    if save_anim:
        save_anim(camera)

    return data_for_ABC


print(revised_ABC())