#!/usr/bin/python
import Adafruit_SSD1306

from PIL import Image

# Raspberry Pi pin configuration:
RST = 24

# display configuration
d1 = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
d2 = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3D)

d1.begin()
d1.clear()
d1.display()

d2.begin()
d2.clear()
d2.display()

imageA = Image.new('1', (128, 64), color=0)
imageB = Image.new('1', (128, 64), color=1)

while True:
	
	d1.image(imageA)
	d2.image(imageB)
	d1.display()
	d2.display()
	
	d1.image(imageB)
	d2.image(imageA)
	d1.display()
	d2.display()
