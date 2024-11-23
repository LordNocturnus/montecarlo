import numpy as np
import matplotlib.pyplot as plt

from src.simulation import Simulation

# run sim
sim = Simulation(runs=1, weeks=500, exp_parameter=0.3)
sim.run()

# postprocess data collected
# total_downtime = sim.down_time_sim()

print(sim.mean_sojourn_time())

# print(sim.sojourn_times)

# plt.hist(sim.sojourn_times, bins=50)
# plt.show()

# plt.scatter(sim.end_times, sim.sojourn_times)
# plt.show()
