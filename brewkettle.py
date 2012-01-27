import serial
import numpy as np
from numpy.random import random_integers
from enable.api import ComponentEditor
from traits.api import HasTraits, Float, Instance, Array, Bool, Button
from traitsui.api import View, Item, Handler, Group, HGroup, TextEditor
from pyface.timer.api import Timer
from chaco.api import Plot, ArrayPlotData, VPlotContainer


class FakeSerial():

    def __init__(self):
        pass

    def write(self, string):
        print string

    def close(self):
        pass

    def readlines(self):
        temperature = 400 + random_integers(0, 100)
        return ["Readlines called on dummy",
                "2," + str(temperature), ";"]


class BrewKettleHandler(Handler):
    def object_dutycycle_to_send_changed(self, info):
        info.object.set_current_dutycycle()

    def object_setpoint_to_send_changed(self, info):
        info.object.set_current_setpoint()


class BrewKettle(HasTraits):
    """ Arduino controlled heatable brew kettle """

    timestamp = Float
    temperature = Float(np.NaN)
    setpoint = Float(np.NaN)
    setpoint_to_send = Float
    send_setpoint = Button
    dutycycle = Float
    dutycycle_to_send = Float
    send_dutycycle = Button
    pid_controlled = Bool
    pump_is_on = Bool
    toggle_pump = Button
    toggle_pid_on_off = Button

    view = View(HGroup(
        Group(
            Item(name="timestamp"),
            Item(name="temperature"),
            Item(name="setpoint"),
            Item(name="dutycycle"),
            Item(name="pid_controlled"),
            Item(name="pump_is_on"),
            label="Latest information from Brew Kettle",
            style="readonly"),
        Group(
            HGroup(Item(name="setpoint_to_send",
                        editor=TextEditor(enter_set=True, auto_set=False,
                                          evaluate=float)),
                   Item(name="send_setpoint", show_label=False)),
            HGroup(Item(name="dutycycle_to_send",
                        editor=TextEditor(enter_set=True, auto_set=False,
                                          evaluate=float)),
                   Item(name="send_dutycycle", show_label=False)),
            Item(name="toggle_pump", show_label=False),
            Item(name="toggle_pid_on_off", show_label=False),
            label="Interact with Brew Kettle")),
        handler=BrewKettleHandler)

    def __init__(self, port="/dev/tty.usbmodem1a21"):

        if port is not None:
            self.serial = serial.Serial(port,
                                        baudrate=57600, timeout=0.1)
        else:
            self.serial = FakeSerial()

        # Print Arduino ready statement, appears only sometimes..
        self.check_for_serial()

    def exit(self):
        self.turn_pump_off()
        self.turn_heater_off()
        self.turn_pid_off()
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

    def turn_pid_on(self):
        self.serial.write("7,1;")
        self.check_for_serial()

    def turn_pid_off(self):
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
        percent = int(np.round(percent))
        self.serial.write("6," + str(percent) + ";")

    def set_current_dutycycle(self):
        self.set_heater_dutycycle(self.dutycycle_to_send)        

    def set_setpoint(self, temperature):
        int_temperature = int(10 * np.round(temperature, 1))
        cmd = "9," + str(int_temperature) + ";"
        print cmd
        self.serial.write(cmd)

    def set_current_setpoint(self):
        self.set_setpoint(self.setpoint_to_send)

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
                self.timestamp = int(cmd_list[1]) / 1000.0
                self.temperature = float(cmd_list[2])
                self.dutycycle = float(cmd_list[3])
                self.setpoint = float(cmd_list[4])
                self.pid_controlled = bool(int(cmd_list[5]))
                self.pump_is_on = bool(int(cmd_list[6]))
            else:
                print line
        self.timestamp += 1

    def _echo_readlines(self):
        for line in self.serial.readlines():
            print line

    def _send_dutycycle_fired(self):
        self.set_current_dutycycle()

    def _send_setpoint_fired(self):
        self.set_current_setpoint()

    def _toggle_pump_fired(self):
        if self.pump_is_on:
            self.turn_pump_off()
        else:
            self.turn_pump_on()

    def _toggle_pid_on_off_fired(self):
        if self.pid_controlled:
            self.turn_pid_off()
        else:
            self.turn_pid_on()


class KettleMonitor(HasTraits):
    temperature_plot = Instance(Plot)
    dutycycle_plot = Instance(Plot)
    plot_container = VPlotContainer()
    time = Array
    temperature = Array
    setpoint = Array
    dutycycle = Array

    def __init__(self, kettle):
        super(KettleMonitor, self).__init__()
        self.kettle = kettle
        self.temperature_data = ArrayPlotData(time=self.time,
                                              temperature=self.temperature,
                                              setpoint=self.setpoint)
        plot = Plot(self.temperature_data)
        plot.plot(("time", "temperature"), color="blue")
        plot.plot(("time", "setpoint"), color="green")
        self.temperature_plot = plot

        self.dutycycle_data = ArrayPlotData(time=self.time,
                                            dutycycle=self.dutycycle)
        plot = Plot(self.dutycycle_data)
        plot.plot(("time", "dutycycle"), color="blue")
        self.dutycycle_plot = plot
        self.plot_container.add(self.dutycycle_plot)
        self.plot_container.add(self.temperature_plot)


    def grab_current_value(self):
        self.time = np.hstack((self.time, kettle.timestamp))
        self.temperature = np.hstack((self.temperature, kettle.temperature))
        self.setpoint = np.hstack((self.setpoint, kettle.setpoint))

    def refresh_plot(self):
        self.temperature_data.set_data("time", self.time)
        self.temperature_data.set_data("temperature", self.temperature)
        self.temperature_data.set_data("setpoint", self.setpoint)
        self.dutycycle_data.set_data("time", self.time)
        self.dutycycle_data.set_data("dutycycle", self.dutycycle)
        self.plot_container.request_redraw()

    kettle = Instance(BrewKettle)
    time = Array
    temperature = Array

    view = View(Group(Item("plot_container", editor=ComponentEditor(),
                           show_label=False),
        label="History plots"),
                resizable=True)


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
        self.timer = Timer(1000, self._timer_callback)
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
        self.monitor.refresh_plot()


if __name__ == "__main__":
    kettle = BrewKettle("/dev/tty.usbmodem1a21")
    demo = Demo(kettle)
    demo.configure_traits()
