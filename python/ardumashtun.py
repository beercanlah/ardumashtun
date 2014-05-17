import serial

kAcknowledge = 0
kError = 1
kFullStatus = 2
kTemperature = 3
kPumpStatus = 4
kHeaterStatus = 5
kDutyCycle = 6
kPIDStatus = 7
kPID = 8
kHeater = 9
kPump = 10
kSetpoint = 11
kPValue = 12
kIValue = 13


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
        self.serial.write(str(kPump) + ',' + str(int(bool(value))) + ';\n\r')

    @property
    def heater(self):
        self._request_value(kHeaterStatus)
        self._echo_readline()

    @property
    def dutycycle(self):
        self._request_value

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
