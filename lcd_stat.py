# Copyright (c) 2015
# Author: Clarence Ho
#
# Python script for Raspberry Pi to show stats on Nokia 5110 screen
#
# Based on tutorial on Adafruit
# https://learn.adafruit.com/nokia-5110-3310-lcd-python-library/overview

import time
from datetime import datetime
import psutil

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import Adafruit_DHT

import Image
import ImageDraw
import ImageFont

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Raspberry Pi software SPI config:
# SCLK = 4
# DIN = 17
# DC = 23
# RST = 24
# CS = 8

# Beaglebone Black hardware SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0

# Beaglebone Black software SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SCLK = 'P8_7'
# DIN = 'P8_9'
# CS = 'P8_11'

DHT_PIN = 4
DHT_SENSOR = Adafruit_DHT.DHT11

def formatByte(b):
    if b < 1024:
        return str(b)
    if b < 1048576:
        return str(b / 1024) + "K"
    if b < 1073741824:
        return str(b / 1048576) + "M"
    return str(b / 1073741824) + "G"

def progressBar(draw, x, y, width, height, percent):
    fillWidth = width * percent
    draw.rectangle((x, y, x+width, y+height), outline=0, fill=255)
    draw.rectangle((x, y, x+fillWidth, y+height), outline=0, fill=0)

def logTempHum(temp, hum):
    with open("/home/pi/THlog.csv", "a") as theFile:
        theFile.write("{}\t{}\t{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), temp, hum))
        theFile.close()

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=40)
#disp.begin()

# Clear display.
disp.clear()
disp.display()

humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
logTempHum(temperature, humidity)
lastLogMin = datetime.now().minute

while True:

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white filled box to clear the image.
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.
    # Some nice fonts to try: http://www.dafont.com/bitmap.php
    #font = ImageFont.truetype('fonts/VCR_OSD_MONO_1.001.ttf', 14)

    # Write the stats
    draw.text((0,0), time.strftime("%b%d %H:%M:%S"), font=font)

    draw.text((4,10), "CPU:", font=font)
    progressBar(draw, 29, 12, LCD.LCDWIDTH - 30, 6, psutil.cpu_percent() / 100.0)

    mem = psutil.virtual_memory()
    draw.text((4,18), "MEM:", font=font)
    progressBar(draw, 29, 20, LCD.LCDWIDTH - 30, 6, float(mem.used) / mem.total)

    net = psutil.net_io_counters()
    draw.text((4,26), "NET:{}/{}".format(formatByte(net.bytes_recv), formatByte(net.bytes_sent)), font=font)

    curMin = datetime.now().minute
    if curMin in [0, 15, 30, 45] and lastLogMin <> curMin:
        lastLogMin = curMin
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        logTempHum(temperature, humidity)
    draw.text((8,34), "T:{:.0f}*C H:{:.0f}%".format(temperature, humidity), font=font)

    # Display image.
    disp.image(image)
    disp.display()

    time.sleep(1)

