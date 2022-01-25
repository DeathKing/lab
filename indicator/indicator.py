#!/usr/bin/env python

# Python code to convert an image to ASCII image.
import sys, random, argparse
import numpy as np
import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor

try:
	import curses
except ImportError:
    print('curses is required!')
    exit(1)

COLORS = {
    "BLACK" : curses.COLOR_BLACK,
    "BLUE" : curses.COLOR_BLUE,
    "CYAN" : curses.COLOR_CYAN,
    "GREEN" : curses.COLOR_GREEN,
    "MAGENTA" : curses.COLOR_MAGENTA,
    "RED" : curses.COLOR_RED,
    "WHITE" : curses.COLOR_WHITE,
    "YELLOW" : curses.COLOR_YELLOW,
    "DEFAULT": -1
}


# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '

def getAverageL(image):

	"""
	Given PIL Image, return average value of grayscale value
	"""
	# get image as numpy array
	im = np.array(image)

	# get shape
	w,h = im.shape

	# get average
	return np.average(im.reshape(w*h))

PIXLE_PER_ROW = 10
PIXLE_PER_COL = 5

def covertImageToAscii(image, rows, cols, moreLevels):
	"""
	Given Image and dims (rows, cols) returns an m*n list of Images
	"""
	# declare globals
	global gscale1, gscale2

	# open image and convert to grayscale
	image = image.convert('L')

	# store dimensions
	W, H = image.size[0], image.size[1]
	
	# ascii image is a list of character strings
	aimg = []
	# generate list of dimensions
	for j in range(rows):
		y1 = int(j*PIXLE_PER_ROW)
		y2 = int((j+1)*PIXLE_PER_ROW)

		# correct last tile
		if j == rows-1:
			y2 = H

		# append an empty string
		aimg.append("")

		for i in range(cols):

			# crop image to tile
			x1 = int(i*PIXLE_PER_COL)
			x2 = int((i+1)*PIXLE_PER_COL)

			# correct last tile
			if i == cols-1:
				x2 = W

			# crop image to extract tile
			img = image.crop((x1, y1, x2, y2))

			# get average luminance
			avg = int(getAverageL(img))

			# look up ascii char
			if moreLevels:
				gsval = gscale1[int((avg*69)/255)]
			else:
				gsval = gscale2[int((avg*9)/255)]

			# append ascii char to string
			aimg[j] += gsval
	
	# return txt image
	return aimg

# main() function
def main(stdscr):


	# create parser
	descStr = "This program converts an image into ASCII art."
	parser = argparse.ArgumentParser(description=descStr)
	# add expected arguments
	parser.add_argument('--letter', dest='letter', required=False, default='0')
	parser.add_argument('--fore-color', dest='foreColor', required=False, default='red')
	parser.add_argument('--back-color', dest='backColor', required=False, default='default')
	#parser.add_argument('--file', dest='imgFile', required=True)
	#parser.add_argument('--scale', dest='scale', required=False)
	#parser.add_argument('--out', dest='outFile', required=False)
	#parser.add_argument('--cols', dest='cols', required=False)
	parser.add_argument('--morelevels',dest='moreLevels',action='store_true')

	# parse args
	args = parser.parse_args()

	curses.curs_set(0)
	curses.use_default_colors()
	curses.init_pair(9, COLORS[args.foreColor.upper()], COLORS[args.backColor.upper()])
	stdscr.bkgd(curses.color_pair(9))
	curses.start_color()

	# Your application can determine the size of the screen by using the curses.LINES
	# and curses.COLS variables to obtain the y and x sizes.
	# Legal coordinates will then extend from (0,0) to (curses.LINES - 1, curses.COLS - 1).
	height, width = stdscr.getmaxyx()

	# set cols
	cols = width
	#if args.cols:
	#	cols = int(args.cols)

	imgHeight, imgWidth = height * PIXLE_PER_ROW, width * PIXLE_PER_COL

	image = Image.new('RGB', (imgWidth, imgHeight), (255, 255, 255))

	font = ImageFont.truetype('./Arial Black.ttf', 360)
	area = font.getsize(args.letter)

	draw = ImageDraw.Draw(image)
	x, y = (imgWidth-area[0])/2, (imgHeight-area[1])/2
	draw.text((x, y), args.letter, font=font, fill=ImageColor.getrgb('red'))

	#print('generating ASCII art...')
	# convert image to ascii txt
	aimg = covertImageToAscii(image, height, width, args.moreLevels)
	
	# stdscr.addstr(1, 0, f"row{height}, col{width}")
	# stdscr.addstr(2, 0, f"imgHeight{imgHeight}, imgWidth{imgWidth}")
	# stdscr.addstr(3, 0, f"row aimg{len(aimg)} col aimg{len(aimg[0])}")
	# write to file
	for idx, row in enumerate(aimg):
		#stdscr.addstr(idx+1, 1, f"{len(row)}")
		stdscr.addstr(idx, 0, row[0:cols-1])

	stdscr.border()
	stdscr.refresh()
	stdscr.getkey()


# call main
if __name__ == '__main__':
	curses.wrapper(main)

