# Boids Simulation

This project is a simple Boids simulation written in Python using `matplotlib`.

## Overview

* Simulates flocking behavior with multiple agents (boids).
* Boids follow basic rules:

  * **Separation:** avoid crowding neighbors.
  * **Alignment:** match velocity with nearby boids.
  * **Cohesion:** move towards the center of nearby boids.
* Boids bounce off the screen edges instead of wrapping around.
* Maximum speed is limited to prevent exponential acceleration.

## Usage

1. Install required packages:

```bash
uv pip install matplotlib
```

2. Run the simulation:

```bash
python boids.py
```

3. To save a lightweight video of the simulation, set `save=True` in the `simulation` call.

The simulation runs in an 800x800 window and display 200 boids by default.
