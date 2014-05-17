from ardumashtun import UnoMashtun

if __name__ == '__main__':
    tun = UnoMashtun('/dev/tty.usbmodem1411')

    print 'Testing temperature'
    tun.temperature

    print 'Testing pumpStatus'
    tun.pump_status

    tun.serial.close()
