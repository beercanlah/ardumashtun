import time
import serial
import matplotlib.pyplot as plt
import csv
import os
import brewkettle
reload(brewkettle)

filename = time.strftime("%Y-%m-%d %H:%M") + ".csv"
path = os.path.join("data", filename)
f = open(path, "w")
csv_writer = csv.writer(f)
csv_writer.writerow(["Time [s]", "Temperature [C]"])

kettle = brewkettle.BrewKettle()
kettle.turn_pump_on()
kettle.turn_heater_on()

start = time.time()
previous = 0
while(True):
    try:
        now = time.time()
        if (now - previous > 10):
            temperature = kettle.get_temperature()
            current = now - start
            print "Time:\t\t" + str(current)
            print "Temperature:\t" + str(temperature)
            csv_writer.writerow((current, temperature))
            previous = now
    except KeyboardInterrupt:
        f.close()
        kettle.exit()
        print "Done"
        break
