# PiMetric

A digital pixel-based clock like the LaMetric for the Raspberry Pi and a MAX7219 8x32 Matrix.
Here are a few impressions:

![picture one from the PiMetric (currently time showen)](https://github.com/sebastianbrunnert/PiMetric/blob/master/media/IMG_4897.jpg?raw=true)
![picture one from the PiMetric (currently weather showen; sunny)](https://github.com/sebastianbrunnert/PiMetric/blob/master/media/IMG_4898.jpg?raw=true)
![picture one from the PiMetric (currently unread mails showen)](https://github.com/sebastianbrunnert/PiMetric/blob/master/media/IMG_4899.JPG?raw=true)
![picture one from the PiMetric (currently weather showen; rainy)](https://github.com/sebastianbrunnert/PiMetric/blob/master/media/IMG_4900.jpg?raw=true)
![picture one from the PiMetric (currently weather showen; cloudy)](https://github.com/sebastianbrunnert/PiMetric/blob/master/media/IMG_4902.JPG?raw=true)


# What do you need?

- Raspberry Pi with Raspbian and Python 2.6 or later
- 5x F-M Jumper Wires
- MAX7219 8x32 Matrix (e.g. https://www.amazon.de/kwmobile-Matrix-Modul-Raspberry-Arduino/dp/B06XJ9ZX17/ref=sr_1_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&m=A2N58YCCQNSUNR&qid=1563443029&s=merchant-items&sr=1-1)



# How to use - Hardware

First you have to connect the matrix to the Raspberry Pi. Here is a short explanation. For a detailed tutorial visit https://luma-led-matrix.readthedocs.io/en/latest/install.html
Allow SPI by typing:

- $sudo raspi-config
- select SPI
- select yes and press finish
- reboot your Raspberry Pi

Now connect the matrix to the Raspberry Pi like this:

| Pin on RPI | Matrix Pin |
|--|--|
| 2 | VCC (1) |
| 6 | GND (2) |
| 19 | DIN (3) |
| 24 | CS (4) |
| 23 | CLK (5) |

Normally some 8x8 pieces of the matrix should be activated.



# How to use - Software

- $ sudo usermod -a -G spi,gpio pi
- $ sudo apt-get install build-essential python-dev python-pip libfreetype6-dev libjpeg-dev
- $ sudo -H pip install --upgrade luma.led_matrix
- $ pip install geocoder imaplib
- $ git clone https://github.com/sebastianbrunnert/PiMetric
- $ cd PiMetric/src
- change some variables in pi_metric.py (e.g. by $ nano pi_metric.py)
- set the var open_weather_map_appid to your own OpenWeatherMap API key (register under https://home.openweathermap.org/users/sign_up and your key will be sent by email
)
- if you want to show the number of unread mails on the PiMetric set the var use_mail to True and change imap4_ssl to the imap adress of your mail provider (e.g. Gmail: imap.gmail.com), mail_username to your mail adress and mail_password to your password - !! you also have to allow acces from 3rd Apps https://myaccount.google.com/security and allow IMAP in the Gmail settings !!
- $ python pi_metric.py


# Todo

- build case (maybe 3d-printed) for the PiMetric
- integrate Alexa
- animated icons
- bluetooth support
- spotify support
- (integrate WhatsApp)
- (mobile app)



# Credits

I used the RPi.GPIO libary: https://sourceforge.net/projects/raspberry-gpio-python/
I used luma.led_matrix: https://github.com/rm-hull/luma.led_matrix
I used the OpenWeatherMap API: https://openweathermap.org/api
I used imaplib: https://docs.python.org/2/library/imaplib.html
I used geocoder: https://pypi.org/project/geocoder/

