import numpy as np

from src.simulation import Simulation

# run sim
sim = Simulation(50)
sim.run()

# postprocess data collected
total_downtime = np.sum(np.asarray([sim.down_time_sim(r) for r in range(50)]), 1)

print(np.average(total_downtime)) # average week downtime

print(len(total_downtime[total_downtime >= 4])/len(total_downtime)) # probability of downtime >= 4 days