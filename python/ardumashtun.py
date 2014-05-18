import serial

kAcknowledge = 0
kError = 1
kFullStatus = 2
kTemperature = 3
kPumpStatus = 4
kHeaterStatus = 5
kDutyCycleStatus = 6
kPIDStatus = 7
kSetpointStatus = 8
kPValueStatus = 9
kIValueStatus = 10
kPID = 11
kDutyCycl = 12
kPump = 13
kSetpoint = 14
kPValue = 15
kIValue = 16


class UnoMashtun(object):
    '''
    Class representing mashtun run by Arduino Uno

    To be used together with the uno_mashtun.ino sketch
    '''

    baudrate = 115200

    def __init__(self, port):
        self.serial = self._open_port(port)

    @property
    def temperature(self):
        self._request_value(kTemperature)
        self._echo_readline()

    @property
    def pump(self):
        self._request_value(kPumpStatus)
        self._echo_readline()

    @pump.setter
    def pump(self, value):
        self._send_bool(kPump, value)

    @property
    def heater(self):
        self._request_value(kHeaterStatus)
        self._echo_readline()

    @property
    def dutycycle(self):
        self._request_value(kDutyCycleStatus)
        self._echo_readline()

    @dutycycle.setter
    def dutycycle(self, value):
        self._send_value(kSetpoint, value)

    @property
    def pid(self):
        self._request_value(kPIDStatus)
        self._echo_readline()

    @pid.setter
    def pid(self, value):
        self._send_bool(kPID, value)

    @property
    def setpoint(self):
        self._request_value(kSetpointStatus)
        self._echo_readline()

    @setpoint.setter
    def setpoint(self, value):
        self._send_value(kSetpoint, value)

    @property
    def p_value(self):
        self._request_value(kPValueStatus)
        self._echo_readline()

    @p_value.setter
    def p_value(self, value):
        self._send_value(kPValue, value)

    @property
    def i_value(self):
        self._request_value(kIValueStatus)
        self._echo_readline()

    @i_value.setter
    def i_value(self, value):
        self._send_value(kIValue, value)

    def _open_port(self, port):
        ser = serial.Serial(port, self.baudrate, timeout=5)
        msg = ser.readline()
        print msg
        ser.timeout = 1
        return ser

    def _echo_readline(self):
        msg = self.serial.readline()
        print msg

    def _request_value(self, message_number):
        self._serial_write(str(message_number) + ';')

    def _serial_write(self, string):
        self.serial.write(string + '\n\r')

    def _send_value(self, msg, value):
        self._serial_write(str(msg) + ',' + str(value) + ';')

    def _send_bool(self, msg, boolean):
        self._serial_write(str(msg) + ',' + str(int(bool(boolean))) + ';')
