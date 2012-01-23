import serial
import time


class BrewKettle():
    """ Arduino controlled heatable brew kettle """

    def __init__(self, port="/dev/tty.usbmodem1a21"):
        self.serial = serial.Serial("/dev/tty.usbmodem1a21",
                                    baudrate=57600, timeout=2)
        # Print Arduino ready statement, appears only sometimes..
        time.sleep(2)
        print self.serial.readline()

    def exit(self):
        self.turn_pump_off()
        self.turn_heater_off()
        self.serial.close()

    def get_temperature(self):
        self.serial.write("5;")
        # First line is ack
        string = self.serial.readline()
        print string
        # Second line is data
        string = self.serial.readline()
        # Its of the form CMD,Temperature;
        # so first get rid of , then of ; by splitting
        string = (string.split(",")[1]).split(";")[0]
        return int(string) / 10.0

    def turn_pump_on(self):
        self.serial.write("4,1;")
        self._echo_readlines()

    def turn_pump_off(self):
        self.serial.write("4,0;")
        self._echo_readlines()

    def turn_heater_on(self):
        self.serial.write("6,1;")
        self._echo_readlines()

    def turn_heater_off(self):
        self.serial.write("6,0;")
        self._echo_readlines()

    def _echo_readlines(self):
        for line in self.serial.readlines():
            print line
