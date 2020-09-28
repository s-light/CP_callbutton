#!/usr/bin/env python3
"""Minimal ItsyBitsy RFM69 Example."""

import board
import digitalio
import adafruit_rfm69
from adafruit_debouncer import Debouncer

LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

spi = board.SPI()


##########################################
# buttons
btn_red_pin = digitalio.DigitalInOut(board.A0)
btn_red_pin.direction = digitalio.Direction.INPUT
btn_red_pin.pull = digitalio.Pull.UP
btn_red = Debouncer(btn_red_pin)

##########################################
# RFM69
RADIO_FREQ_MHZ = 433.0
CS = digitalio.DigitalInOut(board.A4)
RESET = digitalio.DigitalInOut(board.A5)

rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm69.encryption_key = None
rfm69.tx_power = 20
rfm69.bitrate = 250000 / 2

print("itsybitsy_rfm69_minimal.py")

while True:
    packet = rfm69.receive()
    if packet is None:
        LED.value = False
    else:
        LED.value = True
        print(
            "{:+.1f}dbm '{}'"
            "".format(
                rfm69.rssi,
                str(packet, "utf-8"),
            ),
        )

        print("send Welcome Here!!")
        rfm69.send(bytes("Welcome Here!!", "utf-8"))

    # check button input
    btn_red.update()
    if btn_red.fell:
        print("send HelloWorld!")
        rfm69.send(bytes("HelloWorld!", "utf-8"))
