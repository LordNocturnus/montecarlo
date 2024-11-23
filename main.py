import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.simulation import Simulation

plt.style.use("ggplot")

for param in [0.1, 0.3]:

    # run sim
    sim = Simulation(runs=1, weeks=500, exp_parameter=param)
    sim.run()

    # OUTPUT THE SOJOURN TIMES
    # Combine the arrays into a DataFrame
    df = pd.DataFrame({'repair end time [days]': sim.end_times, 'sojourn time [days]': sim.sojourn_times})

    # Save to a single CSV file
    df.to_csv("results/sojourns_{}.csv".format(param), index=False)

    # OUTPUT THE WEEKLY TOTALS
    weekly_totals = sim.weekly_total_sojourn()
    df = pd.DataFrame({'week index': np.arange(len(weekly_totals)), 'total weekly sojourn time [days]': weekly_totals})

    # Save to a single CSV file
    df.to_csv("results/weekly_total_{}.csv".format(param), index=False)

    st = sim.sojourn_times
    wt = sim.weekly_total_sojourn()

    # a) plot consecutive pairs
    fig, ax = plt.subplots()

    ax.scatter(st[:-1], st[1:], marker = 'x', s=0.75)
    ax.set_xlabel('$s_j$ [days]')
    ax.set_ylabel('$s_{j+1}$ [days]')

    plt.savefig('results/sojourn_pairs_{}.png'.format(param))
    plt.clf()

    # b) autocorrelations


    for lag in range(1, 9):
        print("autocorrelation for consecutive sojourn times, lag={}:".format(lag))
        print(pd.Series(st).autocorr(lag=lag))

    for lag in range(1, 9):
        print("autocorrelation for weekly totals, lag={}:".format(lag))
        print(pd.Series(wt).autocorr(lag=lag))

    # c) processing

    # 1) no batches:



    # pd.plotting.autocorrelation_plot(st, marker='x')
    # plt.xlim(1, 8)
    # plt.show()





# postprocess data collected
# total_downtime = sim.down_time_sim()

# print(sim.mean_sojourn_time())

# print(sim.sojourn_times)

# plt.hist(sim.sojourn_times, bins=50)
# plt.show()

# plt.scatter(sim.end_times, sim.sojourn_times)
# plt.show()
