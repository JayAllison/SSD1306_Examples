#!/usr/bin/python

# Take some text (like a quote) and scroll it across two SSD1306 displays
# originally derived from Adafruit's shapes.py example
#

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import requests
import subprocess
import time

# Raspberry Pi pin configuration:
RST = 24

# display configuration: my displays are at I2C addr 0x3C and 0x3D (verify with 'sudo i2cdetect -y 1')
i2c_addrs = (0x3D,0x3C)
displays = []

# initialize the two displays
for i2c_addr in i2c_addrs:
	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=i2c_addr)
	disp.begin()
	disp.clear()
	disp.display()
	displays.append(disp)

# how far down the screen should the scrolling text be?
ypos = 16

# how fast (pixels per iteration) should the scrolling occur?
step_size = 16

# how many pixels apart are the two screen edges?
screen_gap = 24

# load our fonts
little_font = ImageFont.truetype("/home/pi/Adafruit_Python_SSD1306/examples/Perfect_DOS_VGA_437.ttf", 16)
big_font = ImageFont.truetype("/home/pi/Adafruit_Python_SSD1306/examples/Perfect_DOS_VGA_437.ttf", 48)

# create an Image and ImageDraw for each screen
screen_image_left = Image.new('1', (128, 64))
screen_draw_left = ImageDraw.Draw(screen_image_left)

screen_image_right = Image.new('1', (128, 64))
screen_draw_right = ImageDraw.Draw(screen_image_right)

images = [screen_image_right, screen_image_left]
draws = [screen_draw_right, screen_draw_left]

# dispatch loop
while True:

	# what text should scroll by?
	scrolling_text = "Hello, my name is Inigo Montoya. You killed my father. Prepare to die."
	try:
		random_quote_response = requests.get("http://quotes.stormconsultancy.co.uk/quotes/random.json")
		if random_quote_response.status_code == requests.codes.ok:
			random_quote_json = random_quote_response.json()
			quote = random_quote_json["quote"]
			author = random_quote_json["author"]
			# these quotes contain unicode characters that do not render correctly in our fonts
			scrolling_text = ('"' + quote + '" - ' + author) \
						.replace(u"\u2019", "'") \
						.replace(u"\u2018", "`") \
						.replace(u"\u2014", "--") \
						.replace(u"\u201c", "\"") \
						.replace(u"\u201d", "\"") \
						.replace(u"\u2013", "-")
	except:
		pass		
	text_size = big_font.getsize(scrolling_text)

	# for efficiency, build a large image up front that will hold the entire rendered text
	text_image = Image.new('1', text_size)
	text_draw = ImageDraw.Draw(text_image)

	if (text_size[1] > 64 - ypos):
		print "ERROR! Font rendered text too tall!"
		exit(1)

	text_draw.text((0, 0), scrolling_text, font=big_font, fill=1)

	# pre-generate all of the screen bitmaps we need to make the scrolling text
	# this is also where we implement the spacing/gap between the screens
	left_screens = []
	for x in range(-2 * screen_image_left.size[0] - screen_gap, text_size[0], step_size):
		window = text_image.crop((x, 0, x + screen_image_left.size[0], text_size[1]))
		left_screens.append(window)

	right_screens = []
	for x in range(-1*screen_image_right.size[0], text_size[0] + screen_image_right.size[0] + screen_gap, step_size):
		window = text_image.crop((x, 0, x + screen_image_right.size[0], text_size[1]))
		right_screens.append(window)

	if len(left_screens) != len(right_screens):
		print "ERROR! screen image buffers must contain the same number of images!"
		exit(1)
	screen_count = len(left_screens)
	screens = [right_screens, left_screens]

	# we don't need to refresh the hostname and IP every single time we draw the screen, 
	# but we should do it frequently in case it changes
	ip = "unknown"
	ip_pieces = str(subprocess.check_output("hostname -I", shell = True)).split()
	if len(ip_pieces):
		ip = ip_pieces[0]
	host = "unknown"
	host_pieces = str(subprocess.check_output("hostname", shell = True)).split()
	if len(host_pieces):
		host = host_pieces[0]
	host_or_ip = [ip, host]

	# for each screen, clear the image and render the static text (host or IP) acros the top
	for (screen_image, screen_draw, id) in zip(images, draws, host_or_ip):
		screen_draw.rectangle((0, 0, screen_image.size[0], screen_image.size[1]), fill=0, outline=0)
		screen_draw.text((0, 0), id, font=little_font, fill=1)

	# now, scroll the message across the bottom portion of the screen
	for x in range(screen_count):

		# we are going to draw the right one then the left one - there is a lot of delay in the draw, 
		# and I prefer the visual effect right-to-left rather than left-to-right
		for (disp, screen, screen_image) in zip(displays, screens, images):

			# paste this window of scrolling text into the screen buffer
			screen_image.paste(screen[x], (0, ypos))

			# write the screen buffer out to the screen
			disp.image(screen_image)
			disp.display()
