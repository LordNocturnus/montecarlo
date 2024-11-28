import numpy.random as npr


class Aircraft:

    def __init__(self, repair_shop, env, seed, exp_parameter, sojourn_time_pointer, end_times_pointer, limit = 500*7,  printing=False):
        self.env = env
        self.repair_shop = repair_shop
        self.rng = npr.default_rng(seed)
        self.printing = printing
        self.id = seed
        self.sojourn_time = sojourn_time_pointer
        self.repair_end_time = end_times_pointer

        self.exp_parameter = exp_parameter

        self.limit = limit

        self.flight_time = 0.0
        self.wait_time = 0.0
        self.repair_time = 0.0

        self.state = 0 # 0 => flying, 1 => waiting 2 => being repaired

        self.action = self.env.process(self.run())

    @property
    def down_time(self):
        return self.wait_time + self.repair_time

    def run(self):

        while self.env.now <= self.limit:

            self.start = self.env.now
            if self.printing:
                print(f"{self.env.now}: Aicraft {self.id} flying")
            self.state = 0
            # Airraft is in flight
            yield self.env.timeout(self.rng.exponential(1/self.exp_parameter))
            self.flight_time += self.env.now - self.start

            with self.repair_shop.request() as req:
                self.start = self.env.now
                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} waiting")
                self.state = 1
                # Airraft is waiting for repair
                yield req
                self.wait_time = self.env.now - self.start

                self.start = self.env.now
                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} repairing")
                # Airraft is being repaired
                self.state = 2
                yield self.env.timeout(self.rng.normal(0.25, 0.05))

                self.repair_time = self.env.now - self.start

                self.sojourn_time.append(self.repair_time + self.wait_time)  # append the (shared sequence with current sojourn time)
                self.repair_end_time.append(self.env.now)

    def post_process(self, limit=7):
        # run for each aircraft after each simulation
        if self.state == 0:
            self.flight_time += limit - self.start
        elif self.state == 1:
            self.wait_time += limit - self.start
        elif self.state == 2:
            self.repair_time += limit - self.start
