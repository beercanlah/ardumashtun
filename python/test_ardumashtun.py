import unittest
import mock
import ardumashtun


class TestMessages(unittest.TestCase):

    @mock.patch('ardumashtun.serial.Serial')
    def test_temperature(self, mock_serial):
        tun = ardumashtun.UnoMashtun('')
        tun.temperature

        mock_serial().write.assert_called_with('3;\n\r')


if __name__ == '__main__':
    unittest.main()
