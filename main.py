import numpy as np

from src.simulation import Simulation

sim = Simulation(50)

sim.run()

total_downtime = np.sum(np.asarray([sim.down_time_sim(r) for r in range(50)]), 1)
avr = np.average(total_downtime)
prob = len(total_downtime[total_downtime >= 4])/len(total_downtime)