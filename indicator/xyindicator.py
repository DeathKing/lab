#!/usr/bin/env python

# Python code to convert an image to ASCII image.
import argparse
import array, fcntl, termios
import numpy as np
import math

from PIL import Image, ImageDraw, ImageFont, ImageColor

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

# 10 levels of gray
GSCALE = '@%#*+=-:. '

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

def covertImageToAscii(image, rows, cols):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    aimg = []
    image = image.convert('L')
    width, height = image.size
    pixel_per_row = height/rows
    pixel_per_col = width/cols

    for j in range(rows):
        y1 = int(j*pixel_per_row)
        y2 = int((j+1)*pixel_per_row)

        if j == rows-1:
            y2 = height

        aimg.append("")

        for i in range(cols):
            x1 = int(i*pixel_per_col)
            x2 = int((i+1)*pixel_per_col)

            if i == cols-1:
                x2 = width

            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageL(img))
            gsval = GSCALE[int((avg*9)/255)]

            aimg[j] += gsval
 
    return aimg

# main() function
def main(stdscr):
    # create parser
    descStr = "This program shows a letter on full terminal screen."
    parser = argparse.ArgumentParser(description=descStr)

    # add expected arguments
    parser.add_argument('--letter', dest='letter', required=False, default='0')
    parser.add_argument('--font-size', dest='fontSize', required=False, default=None)
    parser.add_argument('--fore-color', dest='foreColor', required=False, default='red')
    parser.add_argument('--back-color', dest='backColor', required=False, default='default')

    # parse args
    args = parser.parse_args()

    # initialize curses environment
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(9, COLORS[args.foreColor.upper()], COLORS[args.backColor.upper()])
    stdscr.bkgd(curses.color_pair(9))
    curses.start_color()

    # Your application can determine the size of the screen by using the curses.LINES
    # and curses.COLS variables to obtain the y and x sizes.
    # Legal coordinates will then extend from (0,0) to (curses.LINES - 1, curses.COLS - 1).
    # Legal coordinates will be from (0,0) to (cols-1, rows-1)	
    rows, cols = stdscr.getmaxyx()

    buf = array.array('H', [0,0,0,0])
    fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
    prow, pcol, pxx, pxy = buf
    fontsize = int(min(pxx, pxy) * 0.90)

    if args.fontSize is not None:
        fontsize = int(args.fontSize)

    if prow != rows or pcol != cols:
        print(f"inconsistant row and cols {rows}, {cols} -- {prow}, {pcol}")

    image = Image.new('RGB', (pxx, pxy), (255, 255, 255))
    font = ImageFont.truetype('./Arial Black.ttf', fontsize)
    draw = ImageDraw.Draw(image)
    x, y = pxx / 2, pxy / 2
    draw.text((x, y), args.letter, font=font, fill=ImageColor.getrgb('red'), anchor='mm')

    # convert image to ascii txt
    aimg = covertImageToAscii(image, rows, cols)

    # write to screen
    for idx, row in enumerate(aimg):
        stdscr.addstr(idx, 0, row[0:cols-1])

    stdscr.border()
    stdscr.refresh()
    while stdscr.getkey() != 'q':
        pass

# call main
if __name__ == '__main__':
    curses.wrapper(main)
