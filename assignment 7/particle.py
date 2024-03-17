import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from random import uniform, random 
import math
import os

w = 600
h = 600
velocity_p = 2
project_dir = rf"."
n_dir_trial = len(os.listdir(os.path.join(project_dir, rf"trials")))
n_dir_data = len(os.listdir(os.path.join(project_dir, rf"data")))

class Particle:
    def __init__(self, id) -> None:
        self.pos = np.array([uniform(0, w), uniform(0, h)])
        dir = np.random.rand(2)
        self.dir = dir / np.linalg.norm(dir)
        self.id = id

    def wrap(self):
        if self.pos[0] < 0:
            self.pos[0] += w
        if self.pos[1] < 0:
            self.pos[1] += h
        if self.pos[0] > w:
            self.pos[0] -= w
        if self.pos[1] > h:
            self.pos[1] -= h

    def step(
        self,
        swarm,
        cohesion_strength=0.5,
        aligment_strength=0.02,
        separation_strength=0.1,
    ):
        neighbours, distances = get_neighbours(self.pos, swarm)
        exist_neighbours = neighbours != None

        avg_sin, avg_cos = 0, 0
        avg_p = np.zeros(2)
        avg_d = np.zeros(2)

        # This if is a solution to the problem described below.
        if exist_neighbours:
            for n in neighbours:

                avg_p += +n.pos
                # This tilts the direction to avoid getting too close
                if n != self:
                    away = self.pos - n.pos
                    away = away / norm(away)
                    away *= separation_strength
                    avg_d += away / len(neighbours)

                # This instead is to align to other particles
                rad = np.arctan2(n.pos[1], n.pos[0])
                degree = np.mod(np.degrees(rad), 360)
                avg_sin += np.sin(degree) / len(neighbours)
                avg_cos += np.cos(degree) / len(neighbours)

            # This instead is to align to other particles
            angle = math.atan2(avg_sin, avg_cos)
            # Add randomness to the direction. It makes things flicker if I remember correctly :\
            angle += (random() * 0.5 - 0.25) * aligment_strength

            # Direction is initialized as average dir of neighbors
            self.dir = np.array([math.cos(angle), math.sin(angle)], dtype=float)
            # Make particle avoid getting too close
            self.dir += avg_d

            # This is to tilt the direction as to get close to other particles
            cohesion = (self.pos - avg_p) / len(neighbours)
            cohesion = cohesion / norm(cohesion)
            cohesion *= cohesion_strength
            self.dir += cohesion

        # Normalize direction vector so velocity is always the same
        self.dir = self.dir / norm(self.dir)

        # This is for saving data
        datapoint = [self.pos, self.dir, distances]

        # Finally, change the position based on the direction vector
        self.pos += self.dir * velocity_p
        # Wrap around at the edges
        self.wrap()

        return datapoint

    def __eq__(self, __value: object) -> bool:
        b1 = np.all(self.pos == __value.pos)
        b2 = np.all(self.dir == __value.dir)
        return b1 and b2

    def __repr__(self) -> str:
        return str(self.__dict__)


def get_neighbours(pos, swarm,distance=100):

    neighbours = []
    dist = []
    for p in swarm:

        d = np.linalg.norm(pos - p.pos)

        if d <= distance:
            neighbours.append(p)
            dist.append(d)

    dist_sort = np.argsort(dist)

    if len(neighbours) > 1:
        return [neighbours[i] for i in dist_sort], [dist[i] for i in dist_sort][1]
    else:
        return None, None

def nearest_neighbours(swarm):
    nearest_neighbours = []
    for p in swarm:
        _, nearest_neighbour = get_neighbours(p.pos, swarm)
        nearest_neighbours.append(nearest_neighbour)
    return nearest_neighbours

def norm(vect):
    return math.sqrt(vect[0] ** 2 + vect[1] ** 2)


def run_nodraw(swarm):
    data = []
    for p in swarm:
        datapoint = p.step(swarm)
        data.append(datapoint)
    return data


def draw(
    swarm,
    cohesion_strength=0.5,
    aligment_strength=0.2,
    separation_strength=0.1,
) -> None:
    data = []
    for p in swarm:
        datapoint = p.step(
            swarm, cohesion_strength, aligment_strength, separation_strength
        )
        data.append(datapoint)
        plt.plot(p.pos[0], p.pos[1], c="black", marker="o", markersize=3)
        plt.arrow(
            p.pos[0],
            p.pos[1],
            p.dir[0] * 10,
            p.dir[1] * 10,
            head_width=2,
            head_length=3,
            fc="blue",
            ec="blue",
        )
        plt.xlim(0, w)
        plt.ylim(0, h)
    return data

def order(swarm):
    diravg = 0
    for p in swarm:
        diravg += (p.dir / norm(p.dir)) / len(swarm)
    return norm(diravg)


def save_anim(camera):
    writergif = animation.PillowWriter(fps=30)
    anim = camera.animate(blit=True)
    anim.save(
        os.path.join(project_dir, rf"trials\\swarm_Motion_{n_dir_trial}.gif"),
        writer=writergif,
    )


def extract_order_for_ABC(data):

    n_prt = len(data[0])
    n_time = len(data)

    order_in_time = []
    for i, row in enumerate(data):

        direction_avg = 0
        for p in row:
            if not any(np.isnan(p[1])):
                dir = p[1] / norm(p[1])
                direction_avg += dir / n_prt

        order_in_time.append(norm(direction_avg))

    avg_order = sum(order_in_time) / len(order_in_time)

    return avg_order