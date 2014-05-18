import unittest
import mock
import ardumashtun


class TestMessages(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('ardumashtun.serial.Serial')
        self.addCleanup(patcher.stop)
        self.mock_serial = patcher.start()
        self.tun = ardumashtun.UnoMashtun('')

    def test_temperature(self):
        self.tun.temperature

        # I need to call this with () because I patched the
        # class and not the instance
        self.mock_serial().write.assert_called_with('3;\n\r')

    def test_pump_status(self):
        self.tun.pump

        self.mock_serial().write.assert_called_with('4;\n\r')


if __name__ == '__main__':
    unittest.main()
