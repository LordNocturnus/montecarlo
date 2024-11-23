import simpy
import numpy as np

from src.aircraft import Aircraft


class Simulation:

    def __init__(self, runs=1, weeks=500, n_machines = 10, exp_parameter=0.3):
        self.runs = runs
        self.weeks = weeks
        self.n_machines = n_machines
        self.exp_parameter = exp_parameter

        # NOTE: does not work for multiple runs
        self.sojourn_times = []  # LIST ACCESSIBLE BY ALL AIRCRAFT (I KNOW THIS IS BAD)
        self.end_times = []  # same as above, storing the end time of each repair

        self.aircraftLog = []

    def run(self):
        """
        main function used for running the simulation(s)
        """
        for run in range(self.runs):
            env = simpy.Environment()

            repair_shop = simpy.Resource(env, 1)

            aircraft = []
            for i in range(self.n_machines):
                aircraft.append(Aircraft(repair_shop, env, run * 10 + i, exp_parameter = self.exp_parameter, sojourn_time_pointer = self.sojourn_times, end_times_pointer = self.end_times, limit=self.weeks * 7))

            # run simulation
            env.run(until=self.weeks * 7)

            # run postprocess for each aircraft
            for a in aircraft:
                a.post_process()
            print(f"finished run {run}")

            # store results
            self.aircraftLog.append(aircraft)
            self.sojourn_times = np.array(self.sojourn_times)  # quality of life
            self.end_times = np.array(self.end_times)

    def down_time_sim(self, sim=0):
        # collect downtime for each aircraft in a specific run
        return np.asarray([a.down_time for a in self.aircraftLog[sim]])

    def mean_sojourn_time(self):
        return np.mean(self.sojourn_times)

