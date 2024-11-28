import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os

from src.simulation import Simulation

plt.style.use("ggplot")

if not os.path.isdir("results"):
    os.mkdir("results")

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
    print(len(st)-1)
    wt = sim.weekly_total_sojourn()

    # a) plot consecutive pairs
    fig, ax = plt.subplots()

    ax.scatter(st[:-1], st[1:], marker = 'x', s=0.75)
    ax.set_xlabel('$s_j$ [days]')
    ax.set_ylabel('$s_{j+1}$ [days]')

    plt.savefig('results/sojourn_pairs_{}.png'.format(param))
    plt.show()
    plt.clf()

    s1_25 = st[:-1][np.logical_and(st[1:] >= 0.25, st[1:] < 0.3)]
    print(len(s1_25))
    s2_25 = st[1:][np.logical_and(st[:-1] >= 0.25, st[:-1] < 0.3)]
    print(len(s2_25))

    fig, ax = plt.subplots()
    ax.hist([s1_25, s2_25], density=True, histtype="bar", label=["0.25<=$S_{j+1}$<0.3", "0.25<=$S_{j}$<0.3"])
    ax.set_xlabel('$s_j$ [days]')
    ax.set_ylabel('probability density [-]')
    ax.legend()

    plt.savefig('results/conditional_25_{}.png'.format(param))
    plt.show()
    plt.clf()

    s1_25 = st[:-1][np.logical_and(st[1:] >= 0.5, st[1:] < 0.6)]
    print(len(s1_25))
    s2_25 = st[1:][np.logical_and(st[:-1] >= 0.5, st[:-1] < 0.6)]
    print(len(s2_25))

    fig, ax = plt.subplots()
    ax.hist([s1_25, s2_25], density=True, histtype="bar", label=["0.5<=$S_{j+1}$<0.55", "0.5<=$S_{j}$<0.55"])
    ax.set_xlabel('$s_j$ [days]')
    ax.set_ylabel('probability density [-]')
    ax.legend()

    plt.savefig('results/conditional_5_{}.png'.format(param))
    plt.show()
    plt.clf()

    """# b) autocorrelations


    for lag in range(1, 9):
        print("autocorrelation for consecutive sojourn times, lag={}:".format(lag))
        print(pd.Series(st).autocorr(lag=lag))
    print('standard error (est): {}'.format(1/np.sqrt(len(st))))

    for lag in range(1, 9):
        print("autocorrelation for weekly totals, lag={}:".format(lag))
        print(pd.Series(wt).autocorr(lag=lag))
    print('standard error (est): {}'.format(1/np.sqrt(len(wt))))

    # c) processing

    # # 1) no batches:
    # mu_1 = np.mean(st)
    # se_1 = np.std(st) / np.sqrt(len(st))
    # print("no batches:")
    # print(mu_1, se_1)
    # 2) batches of size 2 and 10:

    for K in [1, 2, len(st) // 50]:
        # Determine the number of batches
        n_batches = len(st) // K

        # Split x into batches and compute means
        YB = [np.mean(st[i * K:(i + 1) * K]) for i in range(n_batches)]

        mu = np.mean(YB)
        se = np.std(YB) / np.sqrt(n_batches)

        print("{} batches of size {}".format(n_batches, K))
        print(mu, se)

    # d)
    for array in [st]:
        tau = 1.0
        se_autocorrelation = 1/np.sqrt(len(array))
        for lag in range(1, 9):
            rho = pd.Series(array).autocorr(lag=lag)
            # print(rho / se_autocorrelation)
            if np.abs(rho) > 3 *se_autocorrelation:
                tau += 2 * rho

        print(tau)

    #pd.plotting.autocorrelation_plot(st, marker='x')
    #plt.xlim(1, 8)
    #plt.show()"""





# postprocess data collected
# total_downtime = sim.down_time_sim()

# print(sim.mean_sojourn_time())

# print(sim.sojourn_times)

# plt.hist(sim.sojourn_times, bins=50)
# plt.show()

# plt.scatter(sim.end_times, sim.sojourn_times)
# plt.show()
