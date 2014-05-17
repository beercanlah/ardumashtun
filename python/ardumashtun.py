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
kPID = 9
kDutyCycle = 10
kPump = 11
kSetpoint = 12
kPValue = 13
kIValue = 14


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
        self.serial.write(str(kDutyCycle) + ',' + str(value) + ';\n\r')

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
        self.serial.write(str(message_number) + ';\n\r')

    def _send_bool(self, msg, boolean):
        self.serial.write(str(msg) + ',' + str(int(bool(boolean))) + ';\n\r')
