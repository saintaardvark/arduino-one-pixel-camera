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


def read_sensor(samples=10):
    """
    Read sensor value in range 0-65535.

    Reads 10 times in quick succession and returns the mean.
    """
    total = 0
    for i in range(samples):
        total += sensor.read_u16()
        sleep(0.05)

    return int(total / samples)


def swing_x(s):
    """
    Swing just a little in the x direction
    """
    s.position(X_SERVO, degrees=0)
    sleep(0.2)
    stop_x(s)


def move_and_read(s, x, dir: str = "up"):
    """
    Move in dir and read measurements.

    dir: either 'up' or 'down'
    """
    if dir == "up":
        start = 0
        end = MAX_Y + 1
        step = 1
    elif dir == "down":
        start = MAX_Y
        end = -1
        step = -1
    else:
        raise ValueError(f"Unknown direction {dir}, should be either 'up' or 'down'")
    for y in range(start, end, step):
        s.position(Y_SERVO, y)
        msm = read_sensor()
        msg = f"XXXXX {x} YYYYY {y} VAL {msm}"
        print(msg)
        sleep(SLEEPYTIME)


def main():
    s = get_s()
    while True:
        # Stop x servo
        print("Stopping x servo...")
        stop_x(s)
        print("Press <enter> to continue...")
        sys.stdin.readline()
        x = 0
        while x < MAX_X:
            # Sweep up x 0 to 90, taking measurements
            # print(f"Y iteration {y} of {MAX_Y_SWINGS}")
            move_and_read(s, x, dir="up")
            swing_x(s)
            x += 1
            move_and_read(s, x, dir="down")
            swing_x(s)
            x += 1
        print("END END END")


if __name__ == "__main__":
    main()
