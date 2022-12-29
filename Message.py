from content import Content
from port import Port
from model import Model
from typing import Any


class Message:

    def __init__(self, source: Model, time : float, content: Any):
        self.source = source
        self.time = time
        self.content = content

    def translate(self, new_port: Port) -> "Message":
        return Message(
            self.source,
            self.time,
            Content(new_port, self.content.value))
