#!/usr/bin/env python3
"""Minimal PyBadge display Example."""

# https://github.com/s-light/cp_stepper_test/blob/master/main.py

import time
import board

import terminalio
from adafruit_display_text import label

from adafruit_pybadger import pybadger


##########################################
# display

display = board.DISPLAY
# display.rotation = 180

print("display_pybadge.py")

##########################################
# functions


def update_display():
    """Update Display Content."""
    text = (
        "{:+.2f} runtime\n"
        # "{:+.2f} °C"
        "{:+.2f} LightLevel"
        "".format(
            time.monotonic(),
            # pybadger.temperatur,
            pybadger.light,
        )
    )
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=12, y=32)
    # splash.append(text_area)
    display.show(text_area)


##########################################
# main


def main():
    """Main."""
    update_display()


print(42 * "*")
print("loop..")
while True:
    main()
