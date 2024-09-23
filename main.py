import numpy as np

from src.simulation import Simulation

sim = Simulation(1)

sim.run()

downtime = np.sum(np.asarray([sim.down_time_sim(r) for r in range(1)]), 1)
