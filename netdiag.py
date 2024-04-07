#!/usr/bin/python3
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import re


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 180
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
backlight.value = True

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
    y += font.getbbox(Eth)[1] + 60
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    y += font.getbbox(IP)[1] + 20
    draw.text((x, y), dns_output, font=font, fill=dns_colour)
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

