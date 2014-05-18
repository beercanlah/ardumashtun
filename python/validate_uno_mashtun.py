import ardumashtun as at
from time import sleep
reload(at)

sleep_time = 0.25

if __name__ == '__main__':
    tun = at.UnoMashtun('/dev/tty.usbmodem1411')

    print 'Testing temperature'
    print tun.temperature

    print 'Turning on pump'
    tun.pump = 1
    sleep(sleep_time)

    print 'Testing pumpStatus'
    print tun.pump

    print 'Turning off pump'
    tun.pump = 0
    sleep(sleep_time)

    print 'Testing pumpStatus again'
    print tun.pump

    print 'Setting duty cycle to 100'
    tun.dutycycle = 100
    sleep(sleep_time)

    print 'Testing duty cycle'
    tun.dutycycle
    sleep(sleep_time)

    print 'Testing heater'
    print tun.heater

    print 'Setting duty cycle to 0'
    tun.dutycycle = 0
    sleep(sleep_time)

    print 'Testing duty cycle again'
    tun.dutycycle

    print 'Testing heater again'
    print tun.heater

    print 'Turning pid off'
    tun.pid = 0
    sleep(sleep_time)

    print 'Testing pid'
    tun.pid

    print 'Turning pid on'
    tun.pid = 1
    sleep(sleep_time)

    print 'Testing pid again'
    tun.pid

    print 'Setting setpoint to 25.0'
    tun.setpoint = 25.0
    sleep(sleep_time)

    print 'Testing setpoint'
    tun.setpoint

    print 'Setting pValue to 10.01'
    tun.p_value = 10.01
    sleep(sleep_time)

    print 'Testing pValue'
    tun.p_value

    print 'Setting iValue to 0.15'
    tun.i_value = 0.15
    sleep(sleep_time)

    print 'Testing iValue'
    tun.i_value

    tun.serial.close()
