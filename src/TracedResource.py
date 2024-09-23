from simpy import Resource
import numpy as np


class TracedResource(Resource):

    def __init__(self, env, capacity):
        super().__init__(env, capacity)
        self.env = env

        self.log_event = []
        self.log_time = []

    def request(self):
        self.log_event.append(1)
        self.log_time.append(self.env.now)
        return super().request()

    def release(self, request):
        self.log_event.append(-1)
        self.log_time.append(self.env.now)
        return super().release(request)

    def availability(self):
        demand = np.cumsum(np.asarray(self.log_event))
        available = self.capacity - demand
        return available, np.asarray(self.log_time)

    def queue_length(self):
        available, time = self.availability()
        available[available > 0] = 0
        return available * -1, time