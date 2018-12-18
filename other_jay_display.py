#!/usr/bin/python

#
# derived from Adafruit's shapes.py example
#

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import time

# Raspberry Pi pin configuration:
RST = 24

# display configuration: my display is at I2C addr 0x3C (verify with 'sudo i2cdetect -y 1')
i2c_addr = 0x3D
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=i2c_addr)

disp.begin()
disp.clear()
disp.display()

# how far down the screen should the scrolling text be?
ypos = 16

# how fast (pixels per iteration) should the scrolling occur?
step_size = 10

# load our font(s)
little_font = ImageFont.truetype("/home/pi/Adafruit_Python_SSD1306/examples/Perfect_DOS_VGA_437.ttf", 16)
big_font = ImageFont.truetype("/home/pi/Adafruit_Python_SSD1306/examples/Perfect_DOS_VGA_437.ttf", 48)

# create an Image and ImageDraw that we will only (?) use to measure the text size
screen_image = Image.new('1', (128, 64))
screen_draw = ImageDraw.Draw(screen_image)

# what text should scroll by?
scrolling_text = "Hello, my name is Inigo Montoya. You killed my father. Prepare to die."
text_size = screen_draw.textsize(scrolling_text, font=big_font)

# for efficiency, build a large image up front that will hold the entire rendered text
text_image = Image.new('1', text_size)
text_draw = ImageDraw.Draw(text_image)

if (text_size[1] > 64 - ypos):
	print "ERROR! Font rendered text too tall!"
	exit(1)

text_draw.text((0, 0), scrolling_text, font=big_font, fill=1)

while True:

	# we don't need to refresh the IP every single time we draw the screen, 
	# but we should do it frequently in case it changes
	ip = "unknown"
	ip_pieces = str(subprocess.check_output("hostname -I", shell = True)).split()
	if len(ip_pieces):
		ip = ip_pieces[0]

	# clear the full display
	screen_draw.rectangle((0, 0, screen_image.size[0], screen_image.size[1]), fill=0, outline=0)

	# render the IP in a small font
	screen_draw.text((0, 0), ip, font=little_font, fill=1)

	# write the image buffer out to the screen
	disp.image(screen_image)
	disp.display()

	for x in range(-1*screen_image.size[0], text_size[0], step_size):

		# copy out the part of the full image that we want to display right now,
		# starting with a screenful of blank to the left 
		# and a ending with a screenful of blank to the right
		window = text_image.crop((x, 0, x + screen_image.size[0], text_size[1]))

		# and paste it into the screen buffer
		screen_image.paste(window, (0, ypos))

		# write the screen buffer out to the screen
		disp.image(screen_image)
		disp.display()
