#!/usr/bin/env python3
"""Simple PyBadge Tone Example."""

import time
from adafruit_pybadger import pybadger

pybadger.play_tone(300, 0.5)
pybadger.play_tone(200, 0.3)
pybadger.play_tone(500, 0.2)
pybadger.play_tone(300, 0.5)
pybadger.play_tone(300, 0.1)
pybadger.play_tone(200, 0.3)
time.sleep(0.1)
pybadger.play_tone(300, 0.5)
pybadger.play_tone(200, 0.3)
pybadger.play_tone(500, 0.2)
pybadger.play_tone(300, 0.5)
pybadger.play_tone(300, 0.1)
pybadger.play_tone(200, 0.3)
