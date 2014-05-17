import serial


class UnoMashtun(object):
    '''
    Class representing mashtun run by Arduino Uno

    To be used together with the uno_mashtun.ino sketch
    '''

    baudrate = 115200

    def __init__(self, port):
        self.port = port

    @property
    def temperature(self):
        port = self._open_port()
        port.close()

    def _open_port(self):
        port = serial.Serial(self.port, self.baudrate, timeout=5)
        ready_msg = port.readline()
        print ready_msg
        port.timeout = 1
        return port
