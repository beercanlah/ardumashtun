import unittest
import mock
import ardumashtun
reload(ardumashtun)


class TestMessagesToArduino(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('ardumashtun.serial.Serial')
        self.addCleanup(patcher.stop)
        self.mock_serial = patcher.start()
        self.tun = ardumashtun.UnoMashtun('')

    def test_temperature(self):
        self.tun.temperature
        self._assert_message_sent(3)

    def test_pump_status(self):
        self.tun.pump
        self._assert_message_sent(4)

    def test_heater_status(self):
        self.tun.heater
        self._assert_message_sent(5)

    def test_dutycycle_status(self):
        self.tun.dutycycle
        self._assert_message_sent(6)

    def test_pid_status(self):
        self.tun.pid
        self._assert_message_sent(7)

    def test_setpoint_status(self):
        self.tun.setpoint
        self._assert_message_sent(8)

    def test_p_value_status(self):
        self.tun.p_value
        self._assert_message_sent(9)

    def test_i_value_status(self):
        self.tun.i_value
        self._assert_message_sent(10)

    def test_pid(self):
        self.tun.pid = 1
        self._assert_message_sent_with_value(11, '1')

    def test_dutycycle(self):
        self.tun.dutycycle = 100
        self._assert_message_sent_with_value(12, '100')

    def test_pump(self):
        self.tun.pump = 1
        self._assert_message_sent_with_value(13, '1')

    def test_setpoint(self):
        self.tun.setpoint = 55.0
        self._assert_message_sent_with_value(14, '55.0')

    def test_p_value(self):
        self.tun.p_value = 10.0
        self._assert_message_sent_with_value(15, '10.0')

    def test_i_value(self):
        self.tun.i_value = 0.15
        self._assert_message_sent_with_value(16, '0.15')

    def _assert_message_sent(self, msg_no):
        # I need to call this with () because I patched the
        # class and not the instance
        self.mock_serial().write.assert_called_with(str(msg_no) + ';\n\r')

    def _assert_message_sent_with_value(self, msg_no, value):
        # I need to call this with () because I patched the
        # class and not the instance
        msg = str(msg_no) + ',' + str(value) + ';\n\r'
        self.mock_serial().write.assert_called_with(msg)


class TestMessagesFromArduino(unittest.TestCase):

        def setUp(self):
            patcher = mock.patch('ardumashtun.serial.Serial')
            self.addCleanup(patcher.stop)
            self.mock_serial = patcher.start()
            self.tun = ardumashtun.UnoMashtun('')

        def test_temperature(self):
            self.tun.serial = self._mocked_serial('3,25.0;')
            self.assertEqual(self.tun.temperature, 25.0)

        def test_pump_status(self):
            self.tun.serial = self._mocked_serial('4,1;')
            self.assertEqual(self.tun.pump, True)

            self.tun.serial = self._mocked_serial('4,0;')
            self.assertEqual(self.tun.pump, False)

        def test_heater_status(self):
            self.tun.serial = self._mocked_serial('5,1;')
            self.assertEqual(self.tun.heater, True)

            self.tun.serial = self._mocked_serial('5,0;')
            self.assertEqual(self.tun.heater, False)

        def test_dutycycle_status(self):
            self.tun.serial = self._mocked_serial('6,1;')
            self.assertEqual(self.tun.dutycycle, True)

            self.tun.serial = self._mocked_serial('6,0;')
            self.assertEqual(self.tun.dutycycle, False)

        def _mocked_serial(self, response):
            mocked_serial = mock.Mock()
            config = {'readline.return_value': response}
            mocked_serial.configure_mock(**config)
            return mocked_serial


if __name__ == '__main__':
    unittest.main()
