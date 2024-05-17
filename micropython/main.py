from machine import Pin, ADC, SoftI2C
import sys
from time import sleep
from servo import Servos

Y_SERVO = 1
X_SERVO = 0
SDA = Pin(22)
SCL = Pin(23)
SLEEPYTIME = 0.2

MAX_Y_SWINGS = 4  # *Actual* number will be 2x this!

sensor = ADC(Pin(4, Pin.IN))


def stop_y(s):
    s.position(Y_SERVO, degrees=90)


def get_s():
    i2c = SoftI2C(scl=SCL, sda=SDA)
    s = Servos(i2c)
    return s


def read_sensor():
    """
    Read sensor value in range 0-65535
    """
    return sensor.read_u16()


def swing_y(s):
    """
    Swing just a little in the y direction
    """
    s.position(Y_SERVO, degrees=0)
    sleep(0.2)
    stop_y(s)


def main():
    s = get_s()
    # Stop y servo
    print("Stopping y servo...")
    stop_y(s)
    print("Press <enter> to continue...")
    sys.stdin.readline()
    y = 0
    while y < MAX_Y_SWINGS:
        # Sweep up x 0 to 90, taking measurements
        print(f"Y iteration {y} of {MAX_Y_SWINGS}")
        for x in range(0, 90):
            s.position(X_SERVO, x)
            msm = read_sensor()
            msg = f"XXXXX {x} YYYYY {y} VAL {msm}"
            print(msg)
            sleep(SLEEPYTIME)
        swing_y(s)
        y += 1
        for x in range(90, 0, -1):
            s.position(X_SERVO, x)
            msm = read_sensor()
            msg = f"XXXXX {x} YYYYY {y} VAL {msm}"
            print(msg)
            sleep(SLEEPYTIME)
        swing_y(s)
        y += 1

    while True:
        sleep(60)


if __name__ == "__main__":
    main()
