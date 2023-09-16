import math
import typing as ty

import typing_extensions as te

from .. import constants, model as mo
from .. import port as po
from . import coordinator as co
from . import base


class Simulator(base.Child[mo.Model]):

    def __init__(self, model: mo.Model, parent: base.Parent) -> None:
        base.Child.__init__(self, model, parent)

    def hold_for(self, sigma: float = constants.INF) -> None:
        self._time_until_event = sigma

    def resume(self, elapsed_time: float) -> None:
        if math.isfinite(self._time_until_event):
            self._time_until_event -= elapsed_time

    def star(self, current_time: float) -> None:
        """
        Generate output.
        Excercise the internal transition.
        And return the next event time.
        """
        # checks if the time agrees with the next event time
        if current_time != self._next_event_time:
            raise ValueError(
                f"Invalid simulator.\
                  Current time does not agree with the next event time."
            )
        # the output function results in a content containing a port and a value
        ports = self._model.output()
        non_empty_ports = list(filter(lambda x: x is not None, ports))
        self._parent.y(current_time, non_empty_ports)

        self._model.internal(current_time)
        self._last_event_time = current_time
        self._next_event_time = current_time + self._model.ta()

        # instead of sending a done message to a parent,
        # this implementation's `star` function just returns.
        self._parent.done(self, self._next_event_time)

    def x(self, t: float, port: po.Port) -> None:
        """
        Excercise the external transition.
        Receives:
            value: the input
            current_time: current global time
        Returns:
            next event time (float)
        """
        if not self._last_event_time <= t <= self._next_event_time:
            raise ValueError(
                f"Invalid simulator.\
                  Current time should be between last and next event times."
            )
        e = t - self._last_event_time
        self._model.external(e, port)
        self._last_event_time = t
        self._next_event_time = t + self._model.ta()

        self._parent.done(self, self._next_event_time)