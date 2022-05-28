# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import math
import sys

from PIL import Image
from PIL import ImageDraw
import ST7735 as ST7735

SPI_SPEED_MHZ = 10  # Higher speed = higher framerate

if len(sys.argv) > 1:
    SPI_SPEED_MHZ = int(sys.argv[1])

print("""
framerate.py - Test LCD framerate.

If you're using Breakout Garden, plug the 0.96" LCD (SPI)
breakout into the rear slot.

Running at: {}MHz
""".format(SPI_SPEED_MHZ))

# Create ST7735 LCD display class.
disp = ST7735.ST7735(
    port=0, # 0 for SPI0 and 1 for SPI1
    cs=0,   # 0 for CE0 and 1 for CE1
    dc=24,
    backlight=19,   # can be any controllable pin
    rst=25,         # can be any controllable pin
    rotation=270,
    invert=False, 
    offset_left=24,
    offset_top=0,
    spi_speed_hz=4000000
)

"""
GPIO pins on Raspberry Pi:
    GND = Any GND pin
    VCC = Any +3.3v pin
    SCL = BCM 11 (SCLK/SCK)
    SDA = BCM 10 (MOSI)
    RES = 25 (Reset)
    DC = 24
    CS = BCM 8 (or BCM 7 depending on CE)
    BLK = BCM 19
"""

WIDTH = disp.width
HEIGHT = disp.height
STEPS = WIDTH * 2
images = []

for step in range(STEPS):
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 128))
    draw = ImageDraw.Draw(image)

    if step % 2 == 0:
        draw.rectangle((79, 0, 159, 79), (0, 128, 0))
    else:
        draw.rectangle((0, 0, 79, 79), (0, 128, 0))

    f = math.sin((float(step) / STEPS) * math.pi)
    offset_left = int(f * WIDTH)
    draw.ellipse((offset_left, 35, offset_left + 10, 45), (255, 0, 0))

    images.append(image)

count = 0
time_start = time.time()

while True:
    disp.display(images[count % len(images)])
    count += 1
    time_current = time.time() - time_start
    if count % 120 == 0:
        print("Time: {:8.3f},      Frames: {:6d},      FPS: {:8.3f}".format(
            time_current,
            count,
            count / time_current))
