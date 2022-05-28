from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ST7735


MESSAGE = "Hello World! How are you today?"

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

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height


img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

draw = ImageDraw.Draw(img)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

size_x, size_y = draw.textsize(MESSAGE, font)

text_x = 160
text_y = (80 - size_y) // 2

t_start = time.time()

while True:
    x = (time.time() - t_start) * 100
    x %= (size_x + 160)
    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
    draw.text((int(text_x - x), text_y), MESSAGE, font=font, fill=(255, 255, 255))
    disp.display(img)
