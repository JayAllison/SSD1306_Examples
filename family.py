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

# initialize the first display
disp1.begin()
disp1.clear()
disp1.display()

# initialize the second display
disp2.begin()
disp2.clear()
disp2.display()

#load the family porttraits
john = Image.open('john.jpg').resize((128, 64), Image.BICUBIC).convert('1')
mark = Image.open('mark.jpg').resize((128, 64), Image.BICUBIC).convert('1')
sarah = Image.open('sarah.jpg').resize((128, 64), Image.BICUBIC).convert('1')
paul = Image.open('paul.jpg').resize((128, 64), Image.BICUBIC).convert('1')

# 
portraits = (john, mark, sarah, paul, john)

while True:
	for i in range(len(portraits)-1):
		disp1.image(portraits[i])
		disp2.image(portraits[i+1])
		disp1.display()
		disp2.display()
		time.sleep(1)
