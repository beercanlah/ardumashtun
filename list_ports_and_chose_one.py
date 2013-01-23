import serial
from traits.api import HasTraits, List, String
from traitsui.api import View, Group, Item, EnumEditor, OKButton, CancelButton
from serial.tools.list_ports import comports


class ComportContainer(HasTraits):
    '''
    Class that represents the available comports on a system
    '''

    comports = List
    selected_port = String

    def __init__(self):
        ports = comports()
        self.comports = []
        # Seems to return list on tuples on mac
        for inner in ports:
            for string in inner:
                self.comports.append(string)

    traits_view = View(
        Group(
            Item(name='selected_port',
                 editor=EnumEditor(name="comports")
                 )),
        buttons=[OKButton, CancelButton])

if __name__ == "__main__":
    ports = ComportContainer()
    ports.configure_traits()
    print ports.selected_port
