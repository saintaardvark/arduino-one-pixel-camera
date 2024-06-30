from machine import ADC, Pin
from time import sleep

from constants import SLEEPYTIME

sensor = ADC(Pin(4, Pin.IN))


def read_sensor(sensor=sensor, samples: int = 10) -> float:
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
