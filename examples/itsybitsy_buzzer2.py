#!/usr/bin/env python3
"""Simple PyBadge Buzzer2 Example."""

import time
import board
import simpleio

while True:
    for f in (262, 294, 330, 349, 392, 440, 494, 523):
        simpleio.tone(board.D5, f, 0.25)  # on for 1/4 second
        time.sleep(0.05)  # pause between notes
    time.sleep(0.5)
