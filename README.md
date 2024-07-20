# One-pixel camera

![A picture of the camera](/assets/IMG_7626.jpeg)
![A picture from the camera, compared with a camera photo of the same scene](/assets/comparison.png)

A one-pixel camera that uses an ESP32, MicroPython, two servos, a
peanut butter jar lid, toilet paper rolls, magnets and scrap wood.  
Inspired by
https://hackaday.com/2015/01/31/a-single-pixel-digital-camera-with-arduino/
(http://chynehome.com/web/index.php/2015/01/29/appareil-photo-de-1-pixel-avec-un-arduino/).

The result is a 90 x 90 pixel greyscale image with heavy distortion,
unexplainable streaks, and terrible dynamic range.

Writeup:
https://hackaday.io/project/197013-my-version-of-the-1-pixel-camera

## Software details

The firmware is written in MicroPython, and is in the `micropython`
directory.  The ESP32 takes readings and logs to the serial port.  

`logger.py` will capture the data, write it out as a CSV file, then
show the image.  You can also use `./show.py` to display the image, or
write out a PNG file.

