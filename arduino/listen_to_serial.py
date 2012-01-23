import serial

serial = serial.Serial("/dev/tty.usbmodem1a21", baudrate=57600, timeout=2)

while True:
    print serial.readline()
