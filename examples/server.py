"""
The servers example

Single Server System:
    Server:
        job 
    ExperimentalFrame:
        generates job (name, time_to_process)
"""
from pydesim.processors.simulator import Simulator
from pydesim.simulation import Simulation
from pydesim.port import Port
from pydesim.content import Content
from pydesim.constants import PASSIVE, INF
from typing import Any
from dataclasses import dataclass
import numpy as np

JOB = "JOB"


@dataclass
class Job:
    name: int
    time: float


class Server(Simulator):
    BUSY = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, in_ports={JOB: Port(self, JOB)}, **kwargs)

    def initialize(self, start_time: float = 0):
        self.jobs = []
        self.state = PASSIVE
        self.time_until_event = INF

    @Simulator.int_transition_wrapper
    def int_transition(self, time: float) -> Any:
        self.jobs.pop(0)
        if self.jobs:
            self.hold_in(Server.BUSY, self.jobs[0].time)
        else:
            self.hold_in(PASSIVE)
        return None

    @Simulator.ext_transition_wrapper
    def ext_transition(self, content: Content, time: float) -> None:
        self.jobs.append(content.value)

        if self.state is Server.BUSY:
            self.resume()
        else:  # state is PASSIVE
            self.hold_in(Server.BUSY, content.value.time)


class ExperimentalFrame(Simulator):
    BUSY = 1

    def __init__(
        self,
        arrival_rate: float,
        job_time_low: float,
        job_time_high: float,
        *args,
        **kwargs
    ):
        super().__init__(*args, out_ports={JOB: Port(self, JOB)}, **kwargs)
        self.arrival_rate = arrival_rate
        self.job_time_low = job_time_low
        self.job_time_high = job_time_high

    def initialize(self, start_time: float):
        self.time_until_event = self.generate_arrival_time()
        self.time_advance(start_time)

    def generate_arrival_time(self) -> float:
        u = np.random.uniform()
        interval = -self.arrival_rate * np.log(u)
        return interval

    def generate_job_time(self) -> float:
        u = np.random.uniform(self.job_time_low, self.job_time_high)
        return u

    @Simulator.int_transition_wrapper
    def int_transition(self, time: float) -> Any:
        self.hold_in(self.state, self.generate_arrival_time())
        job = Job("Job", self.generate_job_time())
        return Content(self.out_ports[JOB], job)


class Recorder:
    def __init__(self) -> None:
        self.data = []

    def count(self, model, args, result):
        self.data.append(len(model.jobs))


if __name__ == "__main__":
    recorder = Recorder()

    job_interval = 2
    job_low = 0
    job_high = 1
    time_limit = 100

    sim = Simulation(name="SingleServer", time_limit=time_limit)
    server = Server(name="Server", int_transition_callbacks=[recorder.count])
    ef = ExperimentalFrame(job_interval, job_low, job_high, name="EF")
    sim.add_children(ef, server)
    sim.couple(ef.out_ports[JOB], server.in_ports[JOB])

    sim.initialize()
    sim.start()
    print(recorder.data)
