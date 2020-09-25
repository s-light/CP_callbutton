#!/usr/bin/env python3
"""Simple PyBadge Pixel Example."""

from adafruit_pybadger import pybadger

while True:
    if pybadger.button.a:
        pybadger.pixels[0] = (0, 0, 1)
    elif pybadger.button.b:
        pybadger.pixels[1] = (50, 0, 100)
    elif pybadger.button.start:
        if pybadger.pixels[4] == (0, 0, 0):
            pybadger.pixels[4] = (100, 100, 100)
        else:
            pybadger.pixels[4] = (0, 0, 0)
