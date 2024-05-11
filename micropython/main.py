from machine import Pin, ADC, SoftI2C
from time import sleep
from servo import Servos

SERVO_IDX = 1
SDA = Pin(22)
SCL = Pin(23)
POT = Pin(15)

blue = Pin(17, Pin.OUT, value=0)
yellow = Pin(5, Pin.OUT, value=0)


def stop(s):
    s.position(SERVO_IDX, degrees=90)


def get_p():
    pot = ADC(POT)
    return pot


def read_degrees(p):
    return int((p.read() / 4095) * 180)


def get_s():
    i2c = SoftI2C(scl=SCL, sda=SDA)
    s = Servos(i2c)
    return s


def sweep(s):
    while True:
        for i in range(0, 180, 10):
            print(i)
            s.position(SERVO_IDX, i)
            sleep(1)
        for i in range(180, 0, -10):
            print(i)
            s.position(SERVO_IDX, i)
            sleep(1)


def slow_rotation(s, p, loops=0):
    """
    Slow rotation.  If loops == 0, loop forever; otherwise,
    do that many loops.
    """
    blue.on()
    yellow.off()
    i = 0
    while True:
        val = read_degrees(p)
        print(f"Slow: {val}...")
        s.position(SERVO_IDX, degrees=val)
        sleep(0.2)
        print("Stop...")
        stop(s)
        print("Wait...")
        sleep(3)
        i += 1
        if loops > 0 and i == loops:
            return


def set_speed(s, p, sleepytime=0.2, loops=0):
    """
    Set speed
    """
    blue.off()
    yellow.on()
    i = 0
    while True:
        val = read_degrees(p)
        print(val)
        s.position(SERVO_IDX, degrees=val)
        sleep(0.2)
        i += 1
        print(loops, i)
        if loops > 0 and i == loops:
            return


def main():
    blue.off()
    yellow.off()
    s = get_s()
    p = get_p()
    while True:
        set_speed(s, p, loops=100)  # shorter loops
        slow_rotation(s, p, loops=20)
