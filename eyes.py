#!/usr/bin/python

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import time

# Raspberry Pi pin configuration:
RST = 24

# display configuration: my displays are I2C addr 0x3C & 0x3D (verify with 'sudo i2cdetect -y 1')
# the display on the left
i2c_addr1 = 0x3C
disp1 = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=i2c_addr1)

# the display on the right
i2c_addr2 = 0x3D
disp2 = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=i2c_addr2)

disp1.begin()
disp1.clear()
disp1.display()

disp2.begin()
disp2.clear()
disp2.display()

image1a = Image.open('basic_eye.bmp')
image2a = Image.open('basic_eye.bmp').transpose(Image.FLIP_LEFT_RIGHT)

image1b = Image.open('closed_eye.bmp')
image2b = Image.open('closed_eye.bmp').transpose(Image.FLIP_LEFT_RIGHT)

while True:

	disp1.image(image1a)
	disp1.display()

	disp2.image(image2a)
	disp2.display()

	time.sleep(2)

	disp1.image(image1b)
	disp1.display()

	disp2.image(image2b)
	disp2.display()

	time.sleep(1)
