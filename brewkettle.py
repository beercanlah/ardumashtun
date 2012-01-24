import serial
import time
import numpy as np


class BrewKettle():
    """ Arduino controlled heatable brew kettle """

    def __init__(self, port="/dev/tty.usbmodem1a21"):
        self.serial = serial.Serial("/dev/tty.usbmodem1a21",
                                    baudrate=57600, timeout=1)
        # Print Arduino ready statement, appears only sometimes..
        self.check_for_serial()
        self.temperature = np.NaN

    def exit(self):
        self.turn_pump_off()
        self.turn_heater_off()
        self.turn_PID_off()
        self.serial.close()

    def get_temperature(self):
        self.serial.write("5;")
        self.check_for_serial()
        return self.temperature

    def turn_PID_on(self):
        self.serial.write("7,1;")
        self.check_for_serial()

    def turn_PID_off(self):
        self.serial.write("7,0;")
        self.check_for_serial()

    def turn_pump_on(self):
        self.serial.write("4,1;")
        self.check_for_serial()

    def turn_pump_off(self):
        self.serial.write("4,0;")
        self.check_for_serial()

    def turn_heater_on(self):
        self.serial.write("7,1;")
        self.check_for_serial()

    def turn_heater_off(self):
        self.serial.write("7,0;")
        self.check_for_serial()

    def set_heater_duty_cycle(self, percent):
        self.serial.write("6," + str(percent) + ";")

    def check_for_serial(self):
        lines_received = self.serial.readlines()
        for line in lines_received:
            # Strip away CR LF
            line = line.rstrip("\r\n")
            
            # If proper command strip away ;
            # else just echo
            if line[-1] is ";":
                line = line[0:-1]
            else:
                print line
            cmd_list = line.split(",")

            # First element is command and an int
            cmd_list[0] = int(cmd_list[0])
            if cmd_list[0] is 2:
                self.temperature = np.round(int(cmd_list[1]) / 10.0, 1)
                print "Temperature received: " + str(self.temperature)
            else:
                print line

    def _echo_readlines(self):
        for line in self.serial.readlines():
            print line
