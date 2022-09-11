from . import Content

class Message:

    def __init__(self, source, time, content):
        self.source = source
        self.time = time
        self.content = content

    def translate(self, new_port):
        return Message(
            self.source,
            self.time,
            Content(new_port, self.content.value))
