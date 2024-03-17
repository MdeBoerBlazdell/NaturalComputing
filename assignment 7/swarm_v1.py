import os
from particle import Particle, draw, nearest_neighbours, order
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from celluloid import Camera
import warnings
import sys
from csv import writer
from seaborn import kdeplot

# Set a new recursion limit
# Be cautious with the value; too high might cause a crash
sys.setrecursionlimit(10000)
warnings.simplefilter(action="ignore", category=RuntimeWarning)
project_dir = rf"."
n_dir_trial = len(os.listdir(os.path.join(project_dir, rf"trials")))
n_dir_data = len(os.listdir(os.path.join(project_dir, rf"data")))

w = 600
h = 600
N = 120 # Number of Boids
time_steps = 300

orders = []
nearest_neighbours_dists = []

with open(
    os.path.join(project_dir, rf"data/swarm_Motion_{n_dir_data}.txt"), "w"
) as file:
    writer = writer(file)

    writer.writerow([f"Particle_{i}, " for i in range(N)])
    swarm = [Particle(i) for i, _ in enumerate(range(0, N))]

    fig = plt.figure()
    camera = Camera(fig)
    

    for _ in range(0, time_steps):
        data = draw(swarm)
        neighbours = nearest_neighbours(swarm)
        nearest_neighbours_dists.append(neighbours)
        camera.snap()
        o = order(swarm)
        orders.append(o)

writergif = animation.PillowWriter(fps=30)
anim = camera.animate(blit=True)
anim.save(
    os.path.join(project_dir, rf"trials/swarm_Motion_{n_dir_trial}_{time_steps}steps.gif"),
    writer=writergif,
)

plt.figure()
plt.plot(orders)
plt.xlabel("Time steps")
plt.ylabel("Order")
plt.title("Order over time")
plt.savefig("Order over time")

plt.figure()
kdeplot(nearest_neighbours_dists[0], label="Generation 0")
kdeplot(nearest_neighbours_dists[99], label="Generation 100")
kdeplot(nearest_neighbours_dists[199], label="Generation 200")
kdeplot(nearest_neighbours_dists[299], label="Generation 300")
plt.xlabel("Distance to nearest neighbour")
plt.ylabel("Count")
plt.legend()
plt.savefig("Distribution over time")