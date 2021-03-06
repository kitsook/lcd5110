![Screenshot](http://3.bp.blogspot.com/-5L1u_x6TsD8/VcaiZ0izL6I/AAAAAAAACTc/jZq5sDXxfkY/s320/IMAG1228.jpg "Photo")

# Nokia 5110 LCD connected to Raspberry Pi
Sample scripts for Raspberry Pi output to Nokia 5110 LCD screen

Reference https://learn.adafruit.com/nokia-5110-3310-lcd-python-library/overview

Naming of pins on my LCD breakout board is a little bit different:
<pre>
Raspberry Pi        5110 LCD
3.3v                Vcc
3.3v                BL
GND                 GND
#23                 DC
#24                 RST
CS0                 CE
SCLK                CLK
MOSI                Din
</pre>

The lcd_stat.py script requires psutil library.  You can install it via
<pre>
$ sudo pip install psutil
</pre>

DHT11 temperature-humidity sensor Python library:
https://github.com/adafruit/Adafruit_Python_DHT
