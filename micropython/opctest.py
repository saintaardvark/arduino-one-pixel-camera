from time import sleep

from constants import X_SERVO, Y_SERVO
from sensor import read_sensor

def y(s, MAX_Y=90, dir: str = "up"):
    """
    s: servo
    dir: direction
    """
    Y_SERVO = 1
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
        print(y)
        sleep(1)
        s.position(Y_SERVO)


def x(s, MAX_X=90, dir: str = "up"):
    """
    s: servo
    dir: direction
    """
    X_SERVO = 0
    if dir == "up":
        start = 0
        end = MAX_X + 1
        step = 1
    elif dir == "down":
        start = MAX_X
        end = -1
        step = -1
    else:
        raise ValueError(f"Unknown direction {dir}, should be either 'up' or 'down'")
    for x in range(start, end, step):
        s.position(X_SERVO, x)
        print(x)
        sleep(1)
        s.position(X_SERVO)

def sensor():
    """
    Print readings form sensor
    """
    while True:
        print(read_sensor())
        sleep(0.5)
