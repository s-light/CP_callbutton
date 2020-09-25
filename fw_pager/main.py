#!/usr/bin/env python3
"""fw_pager."""

import time
import board
import digitalio

import adafruit_rfm69

from adafruit_pybadger import pybadger

from adafruit_debouncer import Debouncer

##########################################
# LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

spi = board.SPI()


##########################################
# RFM69
RADIO_FREQ_MHZ = 433.0

CS = digitalio.DigitalInOut(board.D10)
RESET = digitalio.DigitalInOut(board.D11)
IRQ = digitalio.DigitalInOut(board.D6)

rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

# Optionally set an encryption key (16 byte AES key).
# MUST match both on the transmitter and receiver
# (or be set to None to disable/the default).
# rfm69.encryption_key = (
#     b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
# )
rfm69.encryption_key = None

# activate high power mode
# The transmit power in dBm.
# Can be set to a value from -2 to 20 for high power devices
rfm69.tx_power = 20


##########################################
# display
# use default build in in terminal mode.

##########################################
# buttons
btn_start = Debouncer(lambda: pybadger.button.start == 0)
btn_select = Debouncer(lambda: pybadger.button.select == 0)
btn_a = Debouncer(lambda: pybadger.button.a == 0)
btn_b = Debouncer(lambda: pybadger.button.b == 0)

##########################################
# timestamps
start_time = time.monotonic()


##########################################
# functions
def buttons_handling():
    """Check for Buttons."""
    btn_select.update()
    btn_start.update()
    btn_a.update()
    btn_b.update()

    if btn_select.fell:
        radio_info_print()
        print()
        print()
        send_packet("start_time_reset")
        global start_time
        start_time = time.monotonic()

    if btn_start.fell:
        send_packet("Ich mag Pizza!")

    if btn_a.fell:
        send_packet("Moin Meister!")

    if btn_b.fell:
        send_packet("Meister Moin !!")


def send_packet(text):
    """Send packet."""
    global start_time
    run_time = time.monotonic() - start_time
    rfm69.send(bytes(text, "utf-8"))
    print(
        "{: 3.1f}: "
        "{} "
        "".format(
            run_time,
            text,
        ),
    )
    play_tone(500)


def packet_handling(packet_text):
    """Handle packet."""
    global start_time
    run_time = time.monotonic() - start_time
    print(
        "{: 3.1f}: "
        "{:+.1f}dbm"
        " "
        "'{}'"
        "".format(
            run_time,
            rfm69.rssi,
            packet_text,
        ),
    )
    if "start_time_reset" in packet_text:
        start_time = time.monotonic()
        play_tone(1000)
        play_tone(1000)
    play_tone(300)


def radio_handling():
    """Check for Incoming Packages."""
    packet = rfm69.receive(timeout=0.1)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        LED.value = False
    else:
        LED.value = True
        packet_text = str(packet, "utf-8")
        packet_handling(packet_text)


def radio_info_print():
    """Print out some chip state."""
    print("radio RFM69 settings:")
    print("Frequency: {0}mhz".format(rfm69.frequency_mhz))
    print("Bit rate: {0}kbit/s".format(rfm69.bitrate / 1000))
    print("Frequency deviation: {0}hz".format(rfm69.frequency_deviation))
    print("tx_power: {0}dBm".format(rfm69.tx_power))
    print("last rssi: {0}dBm".format(rfm69.rssi))


def play_tone(frequency=440, duration=0.1):
    """Play Tone on piezo."""
    pybadger.play_tone(frequency, duration)


##########################################
# main
print("fw_pager")
print("press button to send packet")

while True:
    buttons_handling()
    radio_handling()
