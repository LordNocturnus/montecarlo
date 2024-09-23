import numpy.random as npr


class Aircraft:

    def __init__(self, repair_shop, env, seed, printing=True):
        self.env = env
        self.repair_shop = repair_shop
        self.rng = npr.default_rng(seed)
        self.printing = printing
        self.id = seed

        self.flight_time = 0.0
        self.wait_time = 0.0
        self.repair_time = 0.0

        self.action = self.env.process(self.run())

    @property
    def down_time(self):
        return self.wait_time + self.repair_time

    def run(self, limit=7):
        while self.env.now <= limit:
            start_flight = self.env.now
            if self.printing:
                print(f"{self.env.now}: Aicraft {self.id} flying")
            yield self.env.timeout(self.rng.exponential(0.2))
            self.flight_time += self.env.now - start_flight

            with self.repair_shop.request() as req:
                start_wait = self.env.now

                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} waiting")
                yield req
                self.wait_time += self.env.now - start_wait
                start_repair = self.env.now
                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} repairing")
                yield self.env.timeout(self.rng.normal(0.25, 0.05))
                self.repair_time += self.env.now - start_repair
