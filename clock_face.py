#!/usr/bin/python

# draw a clock face on the blue part of my SSD1306 OLED display

import Adafruit_SSD1306
import datetime
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

# define the characteristics of my screen: 128x64, with the first 16 rows yellow and the last 48 rows blue
width = 128
height = 64
yellow_offset = 16

# where my screen is on the I2C bus
RST = 24
i2c_addr = 0x3D
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=i2c_addr)

disp.begin()
disp.clear()
disp.display()

# initialize an Image and ImageDraw
image = Image.new('1', (128, 64))
draw = ImageDraw.Draw(image)

# font for the date
font = ImageFont.truetype("/home/pi/Adafruit_Python_SSD1306/examples/Perfect_DOS_VGA_437.ttf", 15)

# set up the circle center's location
max_blue = height - yellow_offset
circle_radius = max_blue / 2
h_center = width / 2
v_center = circle_radius + yellow_offset

# lay out the outer circle's rim
# make sure the heighth (inclusive) and width (inclusive) are odd so there is an exact center
circle_bottom = height - 1
circle_top = yellow_offset + 1
circle_left = h_center - circle_radius + 1
circle_right = h_center + circle_radius - 1

# lay out a circle at the center
center_radius = 2
center_top = v_center - center_radius
center_bottom = v_center + center_radius
center_left = h_center - center_radius
center_right = h_center + center_radius

hour_scale = 0.6
minute_scale = 0.8
second_scale = 0.7

hour_width = 5
minute_width = 3
second_width = 1

while True:

	# get the current date & time
	now = datetime.datetime.now()
	date = now.strftime("%a %m/%d/%Y")

	# how big is the date? we want to center it.
	datesize = font.getsize(date)
	if (datesize[0] > width):
		print "ERROR! Date font is too wide!"
		exit(0)
	if (datesize[1] > yellow_offset):
		print "ERROR! Date font is too tall!"
		exit(0)
	date_x = (width - datesize[0]) / 2
	date_y = 0

	# where the hour hand should go
	hour_length = circle_radius * hour_scale
	hour_percent = ((now.hour % 12) * 60 + now.minute) / 720.0
	hour_angle = hour_percent * 360
	hour_x = int(round(h_center + math.sin(math.radians(hour_angle)) * hour_length))
	hour_y = int(round(v_center - math.cos(math.radians(hour_angle)) * hour_length))

	# where the minute hand should go
	minute_length = circle_radius * minute_scale
	minute_percent = now.minute / 60.0
	minute_angle = minute_percent * 360
	minute_x = int(round(h_center + math.sin(math.radians(minute_angle)) * minute_length))
	minute_y = int(round(v_center - math.cos(math.radians(minute_angle)) * minute_length))

	# where the second hand should go
	second_length = circle_radius * second_scale
	second_percent = now.second / 60.0
	second_angle = second_percent * 360
	second_x = int(round(h_center + math.sin(math.radians(second_angle)) * second_length))
	second_y = int(round(v_center - math.cos(math.radians(second_angle)) * second_length))

	# create the clock-face image to display
	draw.rectangle((0, 0, width, height), fill=0, outline=0)
	draw.text((date_x, date_y), date, font=font, fill=1)
	draw.ellipse((circle_left, circle_top, circle_right, circle_bottom), fill=0, outline=1)
	draw.line((h_center, v_center, hour_x, hour_y), fill=1, width=hour_width)
	draw.line((h_center, v_center, minute_x, minute_y), fill=1, width=minute_width)
	draw.line((h_center, v_center, second_x, second_y), fill=1, width=second_width)
	draw.ellipse((center_left, center_top, center_right, center_bottom), fill=0, outline=1)

	disp.image(image)
	disp.display()

	time.sleep(0.1)
