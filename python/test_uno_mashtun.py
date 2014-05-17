import ardumashtun as at
reload(at)

if __name__ == '__main__':
    tun = at.UnoMashtun('/dev/tty.usbmodem1411')

    print 'Testing temperature'
    tun.temperature

    print 'Testing pumpStatus'
    tun.pump

    print 'Turning on pump'
    tun.pump = 1

    print 'Testing pumpStatus again'
    tun.pump

    print 'Turning off pump'
    tun.pump = 0

    print 'Testing pumpStatus again'
    tun.pump

    print 'Testing heater'
    tun.heater

    tun.serial.close()
