import serial
import time
import numpy as np

from traits.api import HasTraits, Float, Int

class FakeSerial():

    def __init__(self):
        pass

    def write(self, string):
        print string

    def readlines(self):
        return ["Readlines called on dummy"]

class BrewKettle(HasTraits):
    """ Arduino controlled heatable brew kettle """

    temperature = Float
    setpoint = Float
    dutycycle = Int
    
    def __init__(self, port="/dev/tty.usbmodem1a21"):
        if port is not None:
            self.serial = serial.Serial(port,
                                        baudrate=57600, timeout=1)
        else:
            self.serial = FakeSerial()
            
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

    def get_in_out_set(self):
        self.serial.write("8;")
        self.check_for_serial()
        return (self.temperature,
                self.dutycycle,
                self.setpoint)

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
        self.serial.write("6,1;")
        self.check_for_serial()

    def turn_heater_off(self):
        self.serial.write("6,0;")
        self.check_for_serial()

    def set_heater_dutycycle(self, percent):
        self.serial.write("6," + str(percent) + ";")

    def set_setpoint(self, temperature):
        int_temperature = int(10 * np.round(temperature,1));
        cmd = "9," + str(int_temperature) + ";"
        print cmd
        self.serial.write(cmd)

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
            if cmd_list[0] is "2":
                self.temperature = np.round(int(cmd_list[1]) / 10.0, 1)
                print "Temperature received: " + str(self.temperature)
            elif cmd_list[0] is "3":
                self.temperature = float(cmd_list[1])
                self.dutycycle = float(cmd_list[2])
                self.setpoint = float(cmd_list[3])
            else:
                print line

    def _echo_readlines(self):
        for line in self.serial.readlines():
            print line

if __name__ == "__main__":
    kettle = BrewKettle(None)
    kettle.configure_traits()
