#!/usr/bin/env python3
"""fw_absender."""

import time
import board
import digitalio

import adafruit_rfm69

import displayio
from adafruit_st7789 import ST7789

from adafruit_debouncer import Debouncer

import pulseio

##########################################
# LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

spi = board.SPI()


##########################################
# RFM69
print("init radio")
RADIO_FREQ_MHZ = 433.0

CS = digitalio.DigitalInOut(board.A4)
RESET = digitalio.DigitalInOut(board.A5)
IRQ = digitalio.DigitalInOut(board.D2)

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

# slower bitrate for reliable transmitting
rfm69.bitrate = 250000 / 2


##########################################
# display
displayio.release_displays()
display_bus = displayio.FourWire(
    spi,
    command=board.D10,
    chip_select=board.D12,
    reset=board.D11,
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

##########################################
# buttons
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

##########################################
# piezo
print("init piezo")
piezo = pulseio.PWMOut(board.D5, duty_cycle=0, frequency=440, variable_frequency=True)
print("done")

##########################################
# timestamps
start_time = time.monotonic()


##########################################
# functions


def buttons_handling():
    """Handle function Buttons."""
    btn_red.update()
    btn_yellow.update()
    btn_green.update()
    if btn_red.fell:
        send_packet("red!")

    if btn_yellow.fell:
        send_packet("yellow!")

    if btn_green.fell:
        send_packet("green!")


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


def radio_packet_handling(packet_text):
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
        time.sleep(0.1)
        play_tone(1000)
    play_tone(500)


def radio_handling():
    """Check for Incoming Packages."""
    packet = rfm69.receive(timeout=0.1)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        LED.value = False
    else:
        LED.value = True
        packet_text = str(packet, "utf-8")
        radio_packet_handling(packet_text)


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
    piezo.frequency = frequency
    piezo.duty_cycle = 65535 // 2
    time.sleep(duration)
    piezo.duty_cycle = 0


##########################################
print("absender")
##########################################
radio_info_print()

print("Waiting for packets...")

while True:
    radio_handling()
    buttons_handling()
