import ardumashtun as at
from time import sleep
reload(at)

sleep_time = 0.25

if __name__ == '__main__':
    tun = at.UnoMashtun('/dev/tty.usbmodem1411')

    print 'Testing temperature'
    tun.temperature

    print 'Testing pumpStatus'
    tun.pump

    print 'Turning on pump'
    tun.pump = 1
    sleep(sleep_time)

    print 'Testing pumpStatus again'
    tun.pump

    print 'Turning off pump'
    tun.pump = 0
    sleep(sleep_time)

    print 'Testing pumpStatus again'
    tun.pump

    print 'Setting duty cycle to 100'
    tun.dutycycle = 100

    print 'Testing duty cycle'
    tun.dutycycle
    sleep(sleep_time)

    print 'Testing heater'
    tun.heater

    print 'Setting duty cycle to 0'
    tun.dutycycle = 0
    sleep(sleep_time)

    print 'Testing duty cycle again'
    tun.dutycycle

    print 'Testing heater again'
    tun.heater

    tun.serial.close()
