import time
import csv
import os
import brewkettle
reload(brewkettle)

filename = time.strftime("%Y-%m-%d %H%M") + ".csv"
path = os.path.join("data", filename)

with open(path, "w") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(("Time [s]", "Temperature [C]"))

kettle = brewkettle.BrewKettle()

kettle.turn_pump_on()
kettle.turn_PID_on()

start = time.time()
previous = 0
while(True):
    try:
        now = time.time()
        kettle.check_for_serial()
        if (now - previous > 1):
            temperature, dutycycle, setpoint = kettle.get_in_out_set()
            current = now - start
            print "Time:\t\t" + str(current)
            print "Temperature:\t" + str(temperature)
            print "Duty Cycle:\t" + str(dutycycle)
            print "Setpoint:\t" + str(setpoint)
            with open(path, "a") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow((current, temperature))
            previous = now
    except KeyboardInterrupt:
        f.close()
        kettle.exit()
        print "Done"
        break
