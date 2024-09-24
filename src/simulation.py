import simpy
import numpy as np

from src.aircraft import Aircraft


class Simulation:

    def __init__(self, runs=1):
        self.runs = runs

        self.aircraftLog = []

    def run(self):
        """
        main function used for running the simulation(s)
        """
        for run in range(self.runs):
            env = simpy.Environment()

            repair_shop = simpy.Resource(env, 1)

            aircraft = []
            for i in range(10):
                aircraft.append(Aircraft(repair_shop, env, run * 10 + i))

            # run simulation
            env.run(until=7)
            # run postprocess for each aircraft
            for a in aircraft:
                a.post_process()
            print(f"finished run {run}")

            # store results
            self.aircraftLog.append(aircraft)

    def down_time_sim(self, sim):
        # collect downtime for each aircraft in a specific run
        return np.asarray([a.down_time for a in self.aircraftLog[sim]])
