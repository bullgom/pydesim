"""
The servers example

Single Server System:
    Server:
        job 
    ExperimentalFrame:
        generates job (name, time_to_process)
"""
import dataclasses as dc

import numpy as np

import pydesim as des
from pydesim import port as po


@dc.dataclass
class ServerState(des.model.State):
    jobs: list[float] = dc.field(default_factory=list)

    def __repr__(self) -> str:
        return "PASSIVE" if not self.jobs else f"BUSY{self.jobs}"

    @property
    def busy(self) -> bool:
        return bool(self.jobs)


class Server(des.model.Model):
    _state: ServerState
    _job_port: des.port.Port[float]

    def __init__(self, name: str):
        super().__init__(name)
        self._in_ports.append(des.port.Port[float]("job"))

    @property
    def job_port(self) -> des.port.Port[float]:
        return self._in_ports[0]

    def initialize(self) -> float:
        super().initialize()
        self._state = ServerState()
        return self._remaining_time

    def internal(self, current_time: float) -> None:
        self._state.jobs.pop(0)

        if self._state.busy:
            self.hold_for(self._state.jobs[0])
        else:
            self.hold_for(des.constants.INF)

    def external(self, elapsed_time: float, port: des.port.Port) -> None:
        process_time: float = port.consume()
        self._state.jobs.append(process_time)
        if self._state.busy:
            self.resume(elapsed_time)
        else:
            self.hold_for(process_time)

    def output(self) -> list[des.port.Port]:
        return []


class ExperimentalFrame(des.model.Model):
    BUSY = 1

    def __init__(
        self,
        arrival_rate: float,
        job_time_low: float,
        job_time_high: float,
    ):
        super().__init__("EF")
        self.arrival_rate = arrival_rate
        self.job_time_low = job_time_low
        self.job_time_high = job_time_high
        self._out_ports.append(des.port.Port[float]("job"))

    def initialize(self) -> float:
        time_until_event = self.generate_arrival_time()
        self.hold_for(time_until_event)
        return time_until_event

    def generate_arrival_time(self) -> float:
        u = np.random.uniform()
        interval = -self.arrival_rate * np.log(u)
        return interval

    def generate_job_time(self) -> float:
        u = np.random.uniform(self.job_time_low, self.job_time_high)
        return u

    def internal(self, time: float) -> None:
        self.hold_for(self.generate_arrival_time())

    def output(self) -> list[des.port.Port]:
        job = self.generate_job_time()
        self._out_ports[0].put(job)
        return self._out_ports

    def external(self, elapsed_time: float, port: des.port.Port) -> None:
        return

    @property
    def job_port(self) -> des.port.Port[float]:
        return self._out_ports[0]


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

    system = des.model.CoupledModel("System")
    server = Server("Server")
    ef = ExperimentalFrame(0.3, 1.0, 3.0)
    system.add_children(server, ef)

    root = des.processors.RootCoordinator()

    system_coordinator = des.processors.Coordinator(system, root)
    server_simulator = des.processors.Simulator(server, system_coordinator)
    ef_simulator = des.processors.Simulator(ef, system_coordinator)

    root.adopt(system_coordinator)
    system_coordinator.adopt(server_simulator, ef_simulator)

    system.internal_couplings[ef.job_port].append((server, server.job_port))
    root.run(50)
