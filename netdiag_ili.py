# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import time
import subprocess
import digitalio
import board
import re


from adafruit_rgb_display import (
    hx8357,
    ili9341,
    ssd1331,
    ssd1351,
    st7735,
    st7789,
)

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()


# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=172, height=320, x_offset=34, # 1.47" ST7789
# disp = st7789.ST7789(spi, rotation=270, width=170, height=320, x_offset=35, # 1.9" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True, width=80,       # 0.96" MiniTFT Rev A ST7735R
# disp = st7735.ST7735R(spi, rotation=90, invert=True, width=80,    # 0.96" MiniTFT Rev B ST7735R
# x_offset=26, y_offset=1,
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
disp = ili9341.ILI9341(
    spi,
    rotation=0,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
fontsmall = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = False

while True:
    time_to_sleep=1
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    try:
      IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    except:
      IP = "IP: NotFound"
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    try: 
      CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    except:
      CPU = "Load unknown"
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    try: 
      MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    except:
      MemUsage = "Memory usage unknown"
#    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
#    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
#    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
#    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "ethtool eth0 2>/dev/null | egrep \"Link detected|Speed|Duplex\" | sed -e 's/^\t//g'"
    try:
      Eth = subprocess.check_output(cmd, shell=True).decode("utf-8")
    except:
      Eth = "eth0 not found"
    match = re.findall("Link detected: yes", Eth)  # From your file reading code.   
    display_colour="#FF0000"
    try:
      print (match[0])
      display_colour="#00FF00"
    except:
      print ("Link down")
      display_colour="#DD0000"
      match = "Link detected: no"
#    for content in cmd:
#      if re.search("Link detected: yes", cmd): 
#        print(content) 
#      else:
#        print ("Nothing found")

    cmd = "getent hosts bbc.co.uk"
    try: 
      DNS = subprocess.run(cmd, shell=True)
      if (DNS.returncode == 0):
        dns_output=("DNS ok")
        dns_colour="#00FF00"
      else:
        dns_output=("DNS down")
        dns_colour="#CC0000"
      print (dns_output)
    except:
      dns_output=("DNS not found")
      dns_colour="#FF0000"
    cmd = "curl -s -I https://www.bbc.co.uk/ | egrep \"^HTTP\""
    try:
      curl = subprocess.check_output(cmd, shell=True).decode("utf-8")
    except:
      curl = "HTTP to bbc failed"
    try: 
      curl_match = re.findall("HTTP/2 200", curl)
    except: 
      curl_match = "Error"
    curl_colour="#FF0000"
    try:
      print (curl_match[0])
      curl_colour="#00FF00"
      curl="HTTP OK"
      time_to_sleep=60
    except:
      print ("No curl")
      curl_colour="#FF0000"
      curl="HTTP to bbc failure"
      time_to_sleep=1
#    for content in cmd:
#      if re.search("Link detected: yes", cmd): 

    # Write four lines of text.
    y = top
    draw.text((x, y), Eth, font=fontsmall, fill=display_colour)
    x += font.getbbox(Eth)[1] + 0
    y += font.getbbox(Eth)[1] + 60
    draw.text((x + 90, y + 90), IP, font=fontsmall, fill="#FFFFFF")
    #y += font.getbbox(IP)[1] + 10
    draw.text((x, y), dns_output, font=fontsmall, fill=dns_colour)
    y += font.getbbox(dns_output)[1] + 20
    draw.text((x, y), CPU, font=fontsmall, fill="#FFFF00")
    y += font.getbbox(CPU)[1] + 20
    draw.text((x, y), MemUsage, font=fontsmall, fill="#00FF00")
    y += font.getbbox(MemUsage)[1] + 20
    draw.text((x, y), curl, font=fontsmall, fill=curl_colour)
    y += font.getbbox(curl)[1] + 20
    #print("y = %i" % y)
#    draw.text((x, y), Temp, font=font, fill="#FF00FF")
#    y += font.getbbox(Disk)[1] + 20

    # Display image.
    disp.image(image, rotation)
    time.sleep(time_to_sleep)


