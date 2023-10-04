import unittest as ut
import pydesim as pd


class PortTest(ut.TestCase):
    def test_put_and_consume(self) -> None:
        value = "hello"
        port = pd.Port[str]()
        port.put(value)
        output = port.take()

        self.assertEqual(value, output)

    def test_port_class(self) -> None:
        @pd.port_class
        class Ports:
            hello: pd.Port[int]

        value = 10
        ports = Ports()
        ports.hello.put(value)
        output = ports.hello.take()
        self.assertEqual(value, output)

    def test_port_type_exception(self) -> None:
        with self.assertRaises(pd.port.PortsTypeException):

            @pd.port_class
            class Ports:
                hello: str

    def test_is_port_class(self) -> None:
        @pd.port_class
        class Ports:
            hello: pd.Port[int]

        class NormalClass:
            pass

        self.assertTrue(issubclass(Ports, pd.port.PortClass))
        self.assertFalse(issubclass(NormalClass, pd.port.PortClass))
