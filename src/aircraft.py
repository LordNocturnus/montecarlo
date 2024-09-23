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

        self.state = 0

        self.action = self.env.process(self.run())

    @property
    def down_time(self):
        return self.wait_time + self.repair_time

    def run(self, limit=7):
        while self.env.now <= limit:
            self.start = self.env.now
            if self.printing:
                print(f"{self.env.now}: Aicraft {self.id} flying")
            self.state = 0
            yield self.env.timeout(self.rng.exponential(1/0.2))
            self.flight_time += self.env.now - self.start

            with self.repair_shop.request() as req:
                self.start = self.env.now
                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} waiting")
                self.state = 1
                yield req
                self.wait_time += self.env.now - self.start

                self.start = self.env.now
                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} repairing")
                self.state = 2
                yield self.env.timeout(self.rng.normal(0.25, 0.05))
                self.repair_time += self.env.now - self.start

    def post_process(self, limit=7):
        if self.state == 0:
            self.flight_time += limit - self.start
        elif self.state == 1:
            self.wait_time += limit - self.start
        elif self.state == 2:
            self.repair_time += limit - self.start
