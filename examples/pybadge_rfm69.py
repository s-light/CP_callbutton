#!/usr/bin/env python3
"""Minimal PyBadge RFM69 Example."""

# https://github.com/adafruit/Adafruit_CircuitPython_RFM69/blob/master/examples/rfm69_simpletest.py

# Simple example to send a message and then wait indefinitely for messages
# to be received.  This uses the default RadioHead compatible GFSK_Rb250_Fd250
# modulation and packet format for the radio.
# Author: Tony DiCola
import board
import busio
import digitalio

import adafruit_rfm69

from adafruit_debouncer import Debouncer
from adafruit_pybadger import pybadger


btn_start = Debouncer(lambda: pybadger.button.start == 0)
btn_select = Debouncer(lambda: pybadger.button.select == 0)


# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)


##########################################
# RFM69

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip,
# use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.D10)
RESET = digitalio.DigitalInOut(board.D11)
IRQ = digitalio.DigitalInOut(board.D6)

# Initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
# rfm69.encryption_key = (
#     b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
# )
rfm69.encryption_key = None
rfm69.tx_power = 20
rfm69.bitrate = 250000 / 2


print("rfm69_pybadge.py")

##########################################
# functions


def check_buttons():
    """Check for Buttons."""
    btn_start.update()
    if btn_start.fell:
        # Send a packet.
        # Note you can only send a packet up to 60 bytes in length.
        # This is a limitation of the radio packet size,
        # so if you need to send larger amounts of data
        # you will need to break it into smaller send calls.
        # Each send call will wait for the previous one to finish.
        rfm69.send(bytes("Hello world!\r\n", "utf-8"))
        print("Sent 'Hello world!'")

    btn_select.update()
    if btn_select.fell:
        # Print out some chip state:
        print("Temperature: {0}C".format(rfm69.temperature))
        print("Frequency: {0}mhz".format(rfm69.frequency_mhz))
        print("Bit rate: {0}kbit/s".format(rfm69.bitrate / 1000))
        print("Frequency deviation: {0}hz".format(rfm69.frequency_deviation))


def check_rfm69():
    """Check for Incoming Packages."""
    packet = rfm69.receive(timeout=0.05)
    # Optionally change the receive timeout from its default of 0.5 seconds:
    # packet = rfm69.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        LED.value = False
        # print("Received nothing! Listening again...")
    else:
        # Received a packet!
        LED.value = True
        # print
        print(
            "{:+.1f}dbm '{}'"
            "".format(
                rfm69.rssi,
                str(packet, "utf-8"),
            ),
        )


##########################################
# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 60 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.
print("Waiting for packets...")

while True:
    check_buttons()
    check_rfm69()
