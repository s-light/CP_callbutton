#!/usr/bin/env python3
"""
PyBadge Button with debounce Example.

https://github.com/adafruit/Adafruit_CircuitPython_PyBadger/blob/master/examples/pybadger_button_debouncing.py
"""
import board
import digitalio

from adafruit_debouncer import Debouncer

btn_red_pin = digitalio.DigitalInOut(board.A0)
btn_red_pin.direction = digitalio.Direction.INPUT
btn_red_pin.pull = digitalio.Pull.UP

btn_yellow_pin = digitalio.DigitalInOut(board.A1)
btn_yellow_pin.direction = digitalio.Direction.INPUT
btn_yellow_pin.pull = digitalio.Pull.UP

btn_green_pin = digitalio.DigitalInOut(board.A2)
btn_green_pin.direction = digitalio.Direction.INPUT
btn_green_pin.pull = digitalio.Pull.UP


btn_red = Debouncer(btn_red_pin)
btn_yellow = Debouncer(btn_yellow_pin)
btn_green = Debouncer(btn_green_pin)


def update_buttons():
    """Debouncer."""
    btn_red.update()
    btn_yellow.update()
    btn_green.update()


def handle_buttons():
    """Handle function Buttons."""
    if btn_red.fell:
        print("red pressed")
    if btn_red.rose:
        print("red released")

    if btn_yellow.fell:
        print("yellow pressed")
    if btn_yellow.rose:
        print("yellow released")

    if btn_green.fell:
        print("green pressed")
    if btn_green.rose:
        print("green released")


while True:
    update_buttons()
    handle_buttons()
