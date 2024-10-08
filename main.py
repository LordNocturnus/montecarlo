from matplotlib import pyplot as plt
import numpy as np
import numpy.random as npr

from src.simulation import Simulation

plt.style.use('ggplot')

# run sim
rng = npr.default_rng(0)
repeats = 400
down_time = np.zeros(repeats)
prob = np.zeros(repeats)
stds_time = np.zeros(repeats)
prob_time = np.zeros(repeats)
for i in range(repeats):
    sim = Simulation(50, rng)
    sim.run() #~54ms -> 400 * 27ms = 10.8s

    # postprocess data collected
    total_downtime = np.sum(np.asarray([sim.down_time_sim(r) for r in range(50)]), 1)
    down_time[i] = np.average(total_downtime)
    stds_time[i] = np.std(total_downtime)
    prob[i] = len(total_downtime[total_downtime >= 4])/len(total_downtime)

mean = np.average(down_time)
std = np.std(down_time)
for i in range(1, 4):
    high = len(down_time[down_time >= mean + i * std])
    low = len(down_time[down_time <= mean - i * std])
    print(f">= +{i} std: {high}, {high / repeats * 100}%")
    print(f"<= +{i} std: {low}, {low / repeats * 100}%")


counts, bins = np.histogram(down_time, density=True)
plt.hist(bins[:-1], bins, weights=counts, edgecolor='black')
plt.show()

#print(np.average(total_downtime)) # average week downtime

#print(len(total_downtime[total_downtime >= 4])/len(total_downtime)) # probability of downtime >= 4 days