import serial
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Create a socket that wraps serial connection to Arduino
serial = serial.Serial('/dev/tty.usbmodem1a21', 57600,
                       bytesize=8, timeout=2)

while True:
    message = socket.recv()
    print "Received message: ", message
    serial.write(message)
    socket.send("1")


