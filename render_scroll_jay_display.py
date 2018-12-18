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
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

disp.begin()
disp.clear()
disp.display()

image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)

little_font = ImageFont.truetype("Perfect DOS VGA 437.ttf", 16)
big_font = ImageFont.truetype("Perfect DOS VGA 437.ttf", 48)

# how far down the screen should the scrolling text be?
ypos = 16

# scrolling refresh rate is limited by how quickly the library can render the font on this platform
# scroll step size is our only way to then control the visual speed
step_size = 12

# what text should scroll by?
scrolling_text = "Hello, my name is Inigo Montoya. You killed my father. Prepare to die."
text_size = draw.textsize(scrolling_text, font=big_font)
if (text_size[1] > 64 - ypos):
	print "ERROR! Font rendered text too tall!"
	exit(1)

while True:

	# we don't need to refresh the IP every single time we draw the screen
	ip = str(subprocess.check_output("hostname -I", shell = True)).split()[0]

	# clear the full display
	draw.rectangle((0, 0, image.size[0], image.size[1]), fill=0, outline=0)

	# render the IP in a small font
	draw.text((0, 0), ip, font=little_font, fill=1)

	# write the image buffer out to the screen
	disp.image(image)
	disp.display()

	for x in range(0, text_size[0] + image.size[0], step_size):

		# implement the scroll
		xpos = image.size[0] - x

		# clear the scrolling part of the display
		draw.rectangle((0, ypos, image.size[0], image.size[1]), fill=0, outline=0)

		# on my SSD1306 screen the top 10 pixels are yellow, the bottom 54 pixels are blue
		draw.text((xpos, ypos), scrolling_text, font=big_font, fill=1)

		# write the image buffer out to the screen
		disp.image(image)
		disp.display()

	time.sleep(1)
