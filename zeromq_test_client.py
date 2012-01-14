import zmq
import firmata

class WrappedSerial(object):
    def __init__(self, socket):
        self.socket = socket
    
    def write(self, message):
        self.socket.send(message)
        message = self.socket.recv()
        print message    

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:5555")
arduino = firmata.Arduino('/dev/tty.usbmodem1a21', baudrate=57600)
serial = WrappedSerial(socket)
arduino.serial = serial

arduino.send_string("Hi\nZQM\n")

