from machine import Pin, ADC, SoftI2C
import sys
from time import sleep
from servo import Servos

Y_SERVO = 1
X_SERVO = 0
SDA = Pin(22)
SCL = Pin(23)
SLEEPYTIME = 0.2
MAX_X = 45
MAX_Y = 45

sensor = ADC(Pin(4, Pin.IN))


def stop_x(s):
    s.position(X_SERVO, degrees=90)


def get_s():
    i2c = SoftI2C(scl=SCL, sda=SDA)
    s = Servos(i2c)
    return s


def read_sensor():
    """
    Read sensor value in range 0-65535
    """
    return sensor.read_u16()


def swing_x(s):
    """
    Swing just a little in the x direction
    """
    s.position(X_SERVO, degrees=0)
    sleep(0.2)
    stop_x(s)


def main():
    s = get_s()
    # Stop y servo
    print("Stopping x servo...")
    stop_x(s)
    print("Press <enter> to continue...")
    sys.stdin.readline()
    x = 0
    while x < MAX_X:
        # Sweep up x 0 to 90, taking measurements
        # print(f"Y iteration {y} of {MAX_Y_SWINGS}")
        for y in range(0, MAX_Y):
            s.position(Y_SERVO, y)
            msm = read_sensor()
            msg = f"XXXXX {x} YYYYY {y} VAL {msm}"
            print(msg)
            sleep(SLEEPYTIME)
        swing_x(s)
        x += 1
        for y in range(MAX_Y, 0, -1):
            s.position(Y_SERVO, y)
            msm = read_sensor()
            msg = f"XXXXX {x} YYYYY {y} VAL {msm}"
            print(msg)
            sleep(SLEEPYTIME)
        swing_x(s)
        x += 1

    print("END END END")
    while True:
        sleep(60)


if __name__ == "__main__":
    main()
