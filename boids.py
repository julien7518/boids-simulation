import math
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Self


VISION: float = 50
MINIMUM_DISTANCE: float = 20
COHESION_RATE: float = 0.05
SEPARATION_RATE: float = 0.1
ALINEMENT_RATE: float = 0.1
MAXIMUM_SPEED: float = 6


class Boid:
    def __init__(
        self,
        x: float | None = None,
        y: float | None = None,
        vx: float | None = None,
        vy: float | None = None,
    ) -> None:
        self.position_x: float = x if x is not None else random.uniform(0, 800)
        self.position_y: float = y if y is not None else random.uniform(0, 800)
        self.velocity_x: float = vx if vx is not None else random.uniform(-2, 2)
        self.velocity_y: float = vy if vy is not None else random.uniform(-2, 2)

    def separation(self, others: list[Self]):
        deviation_x: float = 0
        deviation_y: float = 0

        for boid in others:
            if boid != self:
                distance: float = euclidian_distance(self, boid)
                if distance < MINIMUM_DISTANCE:
                    deviation_x += self.position_x - boid.position_x
                    deviation_y += self.position_y - boid.position_y

        self.velocity_x += deviation_x * SEPARATION_RATE
        self.velocity_y += deviation_y * SEPARATION_RATE

    def alignement(self, others: list[Self]):
        total_velocity_x: float = 0
        total_velocity_y: float = 0
        number_of_boids: int = 0

        for boid in others:
            if boid != self:
                distance: float = euclidian_distance(self, boid)
                if distance < VISION:
                    number_of_boids += 1
                    total_velocity_x += boid.velocity_x
                    total_velocity_y += boid.velocity_y

        if number_of_boids:
            average_velocity_x: float = total_velocity_x / number_of_boids
            average_velocity_y: float = total_velocity_y / number_of_boids

            self.velocity_x += (average_velocity_x - self.velocity_x) * ALINEMENT_RATE
            self.velocity_y += (average_velocity_y - self.velocity_y) * ALINEMENT_RATE

    def cohesion(self, others: list[Self]):
        x_center: float = 0
        y_center: float = 0
        number_of_boids: int = 0

        for boid in others:
            if boid != self:
                distance: float = euclidian_distance(self, boid)
                if distance < VISION:
                    number_of_boids += 1
                    x_center += boid.position_x
                    y_center += boid.position_y

        if number_of_boids:
            x_center /= number_of_boids
            y_center /= number_of_boids

            self.velocity_x += (x_center - self.position_x) * COHESION_RATE
            self.velocity_y += (y_center - self.position_y) * COHESION_RATE

    def update_params(self, others: list[Self]) -> None:
        self.alignement(others)
        self.separation(others)
        self.cohesion(others)

        speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        if speed > MAXIMUM_SPEED:
            factor = MAXIMUM_SPEED / speed
            self.velocity_x *= factor
            self.velocity_y *= factor

        self.position_x += self.velocity_x
        self.position_y += self.velocity_y

        if self.position_x > 800:
            self.position_x = 800
            self.velocity_x *= -1
        elif self.position_x < 0:
            self.position_x = 0
            self.velocity_x *= -1

        if self.position_y > 800:
            self.position_y = 800
            self.velocity_y *= -1
        elif self.position_y < 0:
            self.position_y = 0
            self.velocity_y *= -1


def euclidian_distance(first: Boid, second: Boid) -> float:
    return math.sqrt(
        (first.position_x - second.position_x) ** 2
        + (first.position_y - second.position_y) ** 2
    )


# Made with ChatGPT
def simulation(numbers_of_boids: int = 200, save: bool = False):
    boids: list[Boid] = [Boid() for _ in range(numbers_of_boids)]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 800)
    scatter = ax.scatter(
        [boid.position_x for boid in boids], [boid.position_y for boid in boids]
    )

    def update(frame):
        for boid in boids:
            boid.update_params(boids)

        scatter.set_offsets([[boid.position_x, boid.position_y] for boid in boids])
        return (scatter,)

    ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)
    plt.show()

    return ani


if __name__ == "__main__":
    simulation()
