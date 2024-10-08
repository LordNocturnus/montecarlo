import numpy.random as npr
import simpy


class Aircraft:

    def __init__(self, repair_shop, env, idx, rng, printing=True):
        self.env = env
        self.repair_shop = repair_shop
        self.rng = rng
        self.printing = printing
        self.id = idx

        self.flight_time = 0.0
        self.wait_time = 0.0
        self.repair_time = 0.0

        self.action = self.env.process(self.run())

    @property
    def down_time(self):
        return self.wait_time + self.repair_time

    def run(self, limit=7):

        while self.env.now <= limit:
            start = self.env.now
            if self.printing:
                print(f"{self.env.now}: Aicraft {self.id} flying")
            # Airraft is in flight
            try:
                yield self.env.timeout(self.rng.exponential(1/0.2))
            except simpy.Interrupt:
                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} terminated")
                break
            self.flight_time += self.env.now - start

            with self.repair_shop.request() as req:
                start = self.env.now
                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} waiting")
                # Airraft is waiting for repair
                try:
                    yield req
                except simpy.Interrupt:
                    if self.printing:
                        print(f"{self.env.now}: Aicraft {self.id} continuing waiting")
                    yield req
                self.wait_time += self.env.now - start

                start = self.env.now
                if self.printing:
                    print(f"{self.env.now}: Aicraft {self.id} repairing")
                # Airraft is being repaired
                repair_time = self.rng.normal(0.25, 0.05)
                try:
                    yield self.env.timeout(repair_time)
                except simpy.Interrupt:
                    if self.printing:
                        print(f"{self.env.now}: Aicraft {self.id} continuing repairing")
                    yield self.env.timeout(repair_time - self.env.now + start)
                self.repair_time += repair_time


def interrupt(env, aircrafts, limit=7):
    yield env.timeout(limit)
    for a in aircrafts:
        a.action.interrupt()