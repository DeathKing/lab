#!/usr/bin/env python

import array, fcntl, termios
buf = array.array('H', [0, 0, 0, 0])
fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
print(buf)
