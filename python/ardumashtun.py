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
kDutyCycle = 12
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
        return self._request_float(kTemperature)

    @property
    def pump(self):
        return self._request_boolean(kPumpStatus)

    @pump.setter
    def pump(self, value):
        self._send_bool(kPump, value)

    @property
    def heater(self):
        return self._request_boolean(kHeaterStatus)

    @property
    def dutycycle(self):
        return self._request_float(kDutyCycleStatus)

    @dutycycle.setter
    def dutycycle(self, value):
        self._send_value(kDutyCycle, value)

    @property
    def pid(self):
        return self._request_boolean(kPIDStatus)

    @pid.setter
    def pid(self, value):
        self._send_bool(kPID, value)

    @property
    def setpoint(self):
        return self._request_float(kSetpointStatus)

    @setpoint.setter
    def setpoint(self, value):
        self._send_value(kSetpoint, value)

    @property
    def p_value(self):
        return self._request_float(kPValueStatus)

    @p_value.setter
    def p_value(self, value):
        self._send_value(kPValue, value)

    @property
    def i_value(self):
        return self._request_float(kIValueStatus)

    @i_value.setter
    def i_value(self, value):
        self._send_value(kIValue, value)

    def _open_port(self, port):
        ser = serial.Serial(port, self.baudrate, timeout=5)
        # Arduino ready message, might take a few seconds
        ser.readline()
        ser.timeout = 1
        return ser

    def _request_float(self, message_number):
        self._request_value(message_number)
        return float(self._read_and_extract_element())

    def _request_boolean(self, message_number):
        self._request_value(message_number)
        return self._read_and_extract_element() == '1'

    def _read_and_extract_element(self):
        msg_string = self._serial_read()
        msg_string = msg_string[:-1]
        msg_elements = msg_string.split(',')
        return msg_elements[1]

    def _request_value(self, message_number):
        self._serial_write(str(message_number) + ';')

    def _serial_write(self, string):
        self.serial.write((string + '\n\r').encode())

    def _serial_read(self):
        msg_string = self.serial.readline()
        # Remove any linefeeds etc
        msg_string = msg_string.decode().rstrip()

        return msg_string

    def _send_value(self, msg, value):
        self._serial_write(str(msg) + ',' + str(value) + ';')

    def _send_bool(self, msg, boolean):
        self._serial_write(str(msg) + ',' + str(int(bool(boolean))) + ';')
