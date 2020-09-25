#!/usr/bin/env python3
"""Minimal PyBadge display Example."""

# https://github.com/s-light/cp_stepper_test/blob/master/main.py

# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus#boards-with-built-in-displays-3025839-17

import time
import board

import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789

##########################################
# display

displayio.release_displays()
spi = board.SPI()
tft_cs = board.D12
tft_dc = board.D10
tft_res = board.D11

display_bus = displayio.FourWire(
    spi,
    command=tft_dc,
    chip_select=tft_cs,
    reset=tft_res,
)

display = ST7789(
    display_bus,
    rotation=270,
    width=240,
    height=135,
    rowstart=40,
    colstart=53,
)
# display.rotation = 180

print("display_itsybitsy.py")


##########################################
# functions


def update_display():
    """Update Display Content."""
    text = (
        "{:+.2f} runtime\n"
        # "{:+.2f} °C"
        # "{:+.2f} LightLevel"
        # "{:+.2f} °C"
        # "{:+.2f} LightLevel"
        "".format(
            time.monotonic(),
            # pybadger.temperatur,
            # pybadger.light,
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


print(37 * "*")
print("loop..")
while True:
    main()
