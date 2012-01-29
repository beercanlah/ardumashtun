import numpy as np
import matplotlib.pyplot as plt
import os
l = [(os.path.getmtime(x), x) for x in os.listdir(".") if x.startswith("2012-")]
l.sort()
filename = l[-1][-1]
filename
data = np.loadtxt(filename, skiprows=1, delimiter=",")
time = data[:, 0]
temperature = data[:, 1]
dutycycle = data [:, 2]
setpoint = data [:, 3]
try:
    plt.clf()
except:
    pass
plt.plot(time, temperature, "b")
plt.plot(time, setpoint, "b")
plt.twinx()
plt.plot(time, dutycycle, "g")
plt.show()
