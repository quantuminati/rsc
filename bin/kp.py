#!/usr/bin/env python

import sys

if not(len(sys.argv) == 2):
	print "usage: {} key_to_press".format(sys.argv[0])
	exit(1)

import keyboard, time
from time import sleep

available_opts = [
	'tab', "shift+=", "shift+'", 'esc', 'f1', 'f3', 'f4', 'f6', 'f8', 'f9',
	'f10', 'f11', 'f11+shift', 'f12'
]

val = sys.argv[1]
if len(val) > 1 or val < ' ' or val > '~':
	if not(val in available_opts): sys.exit(1)

# It seems like the 'enter' press is more universally compatible across
# all the configurations I tested, along with the slight sleep delay
keyboard.press_and_release('enter')
sleep(.1)
keyboard.press(val)
sleep(.1)
keyboard.release(val)
