#!/usr/bin/env python3
"""
PyBadge Button with debounce Example.

https://github.com/adafruit/Adafruit_CircuitPython_PyBadger/blob/master/examples/pybadger_button_debouncing.py
"""

from adafruit_debouncer import Debouncer
from adafruit_pybadger import pybadger

btn_start = Debouncer(lambda: pybadger.button.start == 0)
btn_select = Debouncer(lambda: pybadger.button.select == 0)
btn_b = Debouncer(lambda: pybadger.button.b == 0)
btn_a = Debouncer(lambda: pybadger.button.a == 0)

btn_up = Debouncer(lambda: pybadger.button.up == 0)
btn_down = Debouncer(lambda: pybadger.button.down == 0)
btn_left = Debouncer(lambda: pybadger.button.left == 0)
btn_right = Debouncer(lambda: pybadger.button.right == 0)


def update_buttons():
    """Debouncer."""
    btn_start.update()
    btn_select.update()
    btn_b.update()
    btn_a.update()
    btn_up.update()
    btn_down.update()
    btn_right.update()
    btn_left.update()


def handle_buttons():
    """Handle function Buttons."""
    if btn_start.fell:
        print("Start pressed")
    if btn_start.rose:
        print("Start released")

    if btn_select.fell:
        print("Select pressed")
    if btn_select.rose:
        print("Select released")

    if btn_b.fell:
        print("B pressed")
    if btn_b.rose:
        print("B released")

    if btn_a.fell:
        print("A pressed")
    if btn_a.rose:
        print("A released")


def handle_buttons_pad():
    """Handle left side navigation Pad Buttons."""
    if btn_up.fell:
        print("UP pressed")
    if btn_up.rose:
        print("UP released")

    if btn_down.fell:
        print("DOWN pressed")
    if btn_down.rose:
        print("DOWN released")

    if btn_right.fell:
        print("RIGHT pressed")
    if btn_right.rose:
        print("RIGHT released")

    if btn_left.fell:
        print("LEFT pressed")
    if btn_left.rose:
        print("LEFT released")


while True:
    update_buttons()
    handle_buttons()
    handle_buttons_pad()
