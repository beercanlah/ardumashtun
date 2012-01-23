import serial

class BrewKettle():
    """ Arduino controlled heatable brew kettle """

    def __init__(self, port="/dev/tty.usbmodem1a21"):
        self.serial = serial.Serial("/dev/tty.usbmodem1a21",
                                    baudrate=57600, timeout=2)
        # Print Arduino ready statement
        print self.serial.readline()
