import time
import serial
import matplotlib.pyplot as plt
import csv
import os
import brewkettle

def get_temperature(serial):
    serial.write("5;")
    # First line is ack
    string = serial.readline()
    print string
    # Second line is data
    string = serial.readline()
    # Its of the form CMD,Temperature;
    # so first get rid of , then of ; by splitting
    string = (string.split(",")[1]).split(";")[0]
    return int(string) / 10.0

filename = time.strftime("%Y-%m-%d %H:%M") + ".csv"
location = os.path.join("data", filename)
csv_writer = csv.writer(open(location, "w"))

serial = serial.Serial("/dev/tty.usbmodem1a21", baudrate=57600,
                       timeout=2)

temperature_list = []
time_list = []
previous = time.time()
while(True):
    try:
        now = time.time()
        if (now - previous > 1):
            temperature = get_temperature(serial)
            time = now - previous
            print "Time:\t\t" + time
            print "Temperature:\t" + temperature
            csv_wrie.writerow(time, temperature)
            previous = now
    except KeyboardInterrupt:
        serial.close()
        print "Done"
        break
