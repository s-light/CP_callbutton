#!/usr/bin/env python3
"""Simple PyBadge Buzzer Example."""

import time
import board
import pulseio

piezo = pulseio.PWMOut(board.D5, duty_cycle=0, frequency=440, variable_frequency=True)

print("buzzer.py")

while True:
    for f in (262, 294, 330, 349, 392, 440, 494, 523):
        piezo.frequency = f
        piezo.duty_cycle = 65535 // 2  # On 50%
        time.sleep(0.25)  # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(0.05)  # Pause between notes
    time.sleep(0.5)
