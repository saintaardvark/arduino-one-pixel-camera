from machine import Pin, ADC, SoftI2C
import sys
from time import sleep
from servo import Servos
from test import test_y

from constants import X_SERVO, Y_SERVO

SDA = Pin(22)
SCL = Pin(23)
SLEEPYTIME = 0.2
MAX_X = 45
MAX_Y = 45

sensor = ADC(Pin(4, Pin.IN))


def stop_x(s):
    s.position(X_SERVO, degrees=90)


def get_s(
    freq: int = 50, min_us: int = 600, max_us: int = 2400, degrees: int = 180
) -> Servos:
    """
    Build & return a pca8695 servo controller object.

    Args:
      freq (int): frequency in Hertz that servo runs at
      min_us (int): minimum duty cycle in microseconds
      max_us (int): maximum duty cycle in microseconds
      degrees (int): degrees that the servo swings

    Returns:
      Servos: servo controller object
    """
    i2c = SoftI2C(scl=SCL, sda=SDA)
    s = Servos(i2c, freq=50, min_us=min_us, max_us=max_us, degrees=degrees)
    return s


def read_sensor(samples: int = 10) -> float:
    """
    Read sensor value in range 0-65535.

    Reads <sample> times in quick succession and returns the mean.

    Args:
      samples (int): how many samples to take

    Returns:
      float: mean of the samples
    """
    total = 0
    for i in range(samples):
        total += sensor.read_u16()
        sleep(SLEEPYTIME / samples)

    return int(total / samples)


def swing_x(s: Servos, degrees: int = 0, sleepytime: float = 0.2):
    """
    Swing just a little in the x direction
    """
    s.position(X_SERVO, degrees)
    sleep(sleepytime)
    stop_x(s)


def move_y_and_read(s, x, dir: str = "up"):
    """
    Move in dir and read measurements.

    Args:
      s: servo object
      x: x position; used for logging
      dir: either 'up' or 'down'
    """
    if dir == "up":
        start = 0
        end = MAX_Y
        step = 1
    elif dir == "down":
        start = MAX_Y -1
        end = -1
        step = -1
    else:
        raise ValueError(f"Unknown direction {dir}, should be either 'up' or 'down'")
    for y in range(start, end, step):
        s.position(Y_SERVO, y)
        msm = read_sensor(samples=100)
        msg = f"XXXXX {x} YYYYY {y} VAL {msm}"
        print(msg)


def main():
    s = get_s()
    while True:
        # Stop x servo
        print("Stopping x servo...")
        stop_x(s)
        print("Press <enter> to continue...")
        sys.stdin.readline()
        print(f"MAX_X {MAX_X} MAX_Y {MAX_Y}")
        # Not sure why, but this is what I need to get the X servo to
        # swing from left to right.
        x = MAX_X
        # count is the X value of the final dataset. It goes up as we
        # swing left to right.
        count = 0
        while x >= 0:
            s.position(X_SERVO, x)
            # Sweep up x 0 to 90, taking measurements
            # print(f"Y iteration {y} of {MAX_Y_SWINGS}")
            move_y_and_read(s, count, dir="up")
            x -= 1
            count += 1
            if count >= MAX_X:
                # Catch the case where MAX_X is set to an odd number;
                # when that happens, count can go beyond it, and the
                # logger will complain about out-of-bounds errors
                break
            s.position(X_SERVO, x)
            move_y_and_read(s, count, dir="down")
            x -= 1
            count += 1
        print("END END END")


if __name__ == "__main__":
    main()
