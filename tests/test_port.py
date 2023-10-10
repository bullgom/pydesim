import unittest as ut
import pydesim as pd


class PortTest(ut.TestCase):
    def test_put_and_consume(self) -> None:
        value = "hello"
        port = pd.Port[str]()
        port.put(value)
        output = port.take()

        self.assertEqual(value, output)
