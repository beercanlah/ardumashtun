import serial
import numpy as np
from numpy.random import random_integers
from traits.api import HasTraits, Enum, Float, Int, Instance, Array
from traitsui.api import View, Item, HGroup, spring, Handler
from pyface.timer.api import Timer
from chaco.chaco_plot_editor import ChacoPlotItem


class FakeSerial():

    def __init__(self):
        pass

    def write(self, string):
        print string

    def readlines(self):
        temperature = 400 + random_integers(0, 100)
        return ["Readlines called on dummy",
                "2," + str(temperature), ";"]


class BrewKettle(HasTraits):
    """ Arduino controlled heatable brew kettle """

    timestamp = Int
    temperature = Float(np.NaN)
    setpoint = Float(np.NaN)
    dutycycle = Float

    view = View(Item(name="temperature"),
                Item(name="setpoint"),
                Item(name="dutycycle"))

    def __init__(self, port="/dev/tty.usbmodem1a21"):
        if port is not None:
            self.serial = serial.Serial(port,
                                        baudrate=57600, timeout=0.5)
        else:
            self.serial = FakeSerial()

        # Print Arduino ready statement, appears only sometimes..
        self.check_for_serial()

    def exit(self):
        self.turn_pump_off()
        self.turn_heater_off()
        self.turn_PID_off()
        self.serial.close()

    def get_temperature(self):
        self.serial.write("5;")
        self.check_for_serial()
        return self.temperature

    def get_all(self):
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
        int_temperature = int(10 * np.round(temperature, 1))
        cmd = "9," + str(int_temperature) + ";"
        print cmd
        self.serial.write(cmd)

    def check_for_serial(self, *args):
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
                self.timestamp = int(cmd_list[1])
                self.temperature = float(cmd_list[2])
                self.dutycycle = float(cmd_list[3])
                self.setpoint = float(cmd_list[4])
            else:
                print line
        self.timestamp += 1

    def _echo_readlines(self):
        for line in self.serial.readlines():
            print line


class KettleMonitor(HasTraits):
    time = Array
    temperature = Array

    def __init__(self, kettle):
        super(KettleMonitor, self).__init__()
        self.kettle = kettle

    def grab_current_value(self):
        self.time = np.hstack((self.time, kettle.timestamp))
        self.temperature = np.hstack((self.temperature, kettle.temperature))

    kettle = Instance(BrewKettle)
    time = Array
    temperature = Array

    view = View(ChacoPlotItem("time", "temperature"))


class DemoHandler(Handler):
    def closed(self, info, is_ok):
        """ Handles a dialog-based user interface being closed by the user.
        Overridden here to stop the timer once the window is destroyed.
        """

        info.object.timer.Stop()
        info.object.kettle.exit()
        return


class Demo(HasTraits):
    kettle = Instance(BrewKettle)
    monitor = Instance(KettleMonitor)
    timer = Instance(Timer)
    view = View(Item("kettle", style="custom", show_label=False),
                Item("monitor", style="custom", show_label=False),
                handler=DemoHandler,
                resizable=True)

    def __init__(self, kettle):
        self.kettle = kettle
        self.monitor = KettleMonitor(kettle)

    def edit_traits(self, *args, **kws):
        # Start up the timer! We should do this only when the demo actually
        # starts and not when the demo object is created.
        self.timer = Timer(1000, self.kettle.check_for_serial)
        return super(Demo, self).edit_traits(*args, **kws)

    def configure_traits(self, *args, **kws):
        # Start up the timer! We should do this only when the demo actually
        # starts and not when the demo object is created.
        self.timer = Timer(1000, self._timer_callback)
        return super(Demo, self).configure_traits(*args, **kws)

    def _timer_callback(self):
        self.kettle.get_all()
        self.kettle.check_for_serial()
        self.monitor.grab_current_value()


if __name__ == "__main__":
    kettle = BrewKettle("/dev/tty.usbmodem1a21")
    demo = Demo(kettle)
    demo.configure_traits()
