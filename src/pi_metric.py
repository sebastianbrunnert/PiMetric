import RPi.GPIO as GPIO
import time
import requests
import geocoder
import imaplib
from datetime import datetime
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219













# !! INSERT YOUR DATA HERE !!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!

# define the OpenWeatherMap API Key
open_weather_map_appid = "YOUR_API_KEY"

# will you use mail support?
use_mail = False
# define IMAP Adress
imap4_ssl = "imap.gmail.com"
# define mail username & password
mail_username = "johndoe@example.com"
mail_password = "password"

# !!!!!!!!!!!!!!!!!!!!!!!!!!!
# !! INSERT YOUR DATA HERE !!














serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=90)

# define the light-uped LEDs
light_uped = []

# define the intern tick of the passage of the loop
tick = 0

# define the location where the icon should be showen
icon_location = [1,2,3,4,5,6,7,8,33,34,35,36,37,38,39,40,65,66,67,68,69,70,71,72,97,98,99,100,101,102,103,104,129,130,131,132,133,134,135,136,161,162,163,164,165,166,167,168,193,194,195,196,197,198,199,200,225,226,227,228,229,230,231,232]

# get location through freegeoip.net
location = geocoder.ip('me').latlng

# the dir for the several letters (numbers represent the activated LEDs on a specific location)
signs = {
    ":": [0,2],
    "1": [1,2,3,5,8,11,14],
    "2": [0,1,2,5,6,7,8,9,12,13,14],
    "3": [0,1,2,5,6,7,8,11,12,13,14],
    "4": [0,2,3,5,6,7,8,11,14],
    "5": [0,1,2,3,6,7,8,11,12,13,14],
    "6": [0,1,2,3,6,7,8,9,11,12,13,14],
    "7": [0,1,2,5,8,11,14],
    "8": [0,1,2,3,5,6,7,8,9,11,12,13,14],
    "9": [0,1,2,3,5,6,7,8,11,14],
    "0": [0,1,2,3,5,6,8,9,11,12,13,14],
    "C": [0,1,2,3,6,9,12,13,14],
    "^": [0,1,2,3],
    "-": [0,1],
    "+": [1,3,4,5,7]
}

# the dir for the icons (numbers represent the activated LEDs on a specific location)
icons = {
    "clock": [10,11,12,13,14,17,20,23,25,28,31,33,34,36,37,38,39,41,47,49,52,55,58,59,60,61,62],
    "weather-rainy": [11,12,13,18,19,20,21,22,25,26,27,28,29,30,31,36,44,50,52,59,60],
    "weather-sunny": [2,5,16,18,19,20,21,23,26,27,28,29,34,35,36,37,40,42,43,44,45,47,58,61],
    "weather-cloudy": [18,19,21,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,49,50,51,52,53,54],
    "weather-snow": [0,3,4,7,9,11,12,14,18,21,24,25,27,28,30,31,32,33,35,36,38,39,42,45,49,51,52,54,56,59,60,63],
    "weather-atmosphere": [54,53,52,51,50,39,38,37,36,34,33,32,17,18,19,20,21],
    "weather-thunderstorm": [4,5,6,11,12,13,18,19,20,25,26,27,35,36,37,43,44,50,51,58],
    "mail": [8,9,10,11,12,13,14,15,16,17,18,21,22,23,24,26,27,28,29,31,32,35,36,39,40,47,48,49,50,51,52,53,54,55]
}

# lights up a specific LED independently from row and column
# 0,1,2,3,4,5 -> 32
# 33,34,35 -> 64
# @arg1: the id of the LED
def light_up(id):
    # check wether ID is rational
    if id>256:
        # crash the program
        print("There can't be an ID above 256!")
        exit()

    y = 1

    # get column and row out of id
    while id>32:
        y = y+1
        id = id-32
    # add to list with light-uped LEDs
    light_uped.append({'x': id-1, 'y': y-1})

# shows a sign on the matrix on a specific location
# @arg1: the array of activated LEDs (normally got out of the signs dir)
# @arg2: array of which LEDs (array with the specific IDs) should display the sign
def show_sign(sign, location):
    # check wether the stated location is big enough to display all activated LEDs of the choosed sign
    if max(sign)+1>len(location):
        # crash the program
        print("The field you choosed isn't big enough!")
        exit()
    # light up each pixel which yield together the sign
    for pixel in sign:
        light_up(location[pixel])

# shows the icon on the outer left 8x8 matrix
# @arg1: the array of activated LEDs (normally got out of the icons dir)
def show_icon(icon):
    for pixel in icon:
        light_up(icon_location[pixel])

# show all necessary information about the time and clears the device before that
def show_time():
    global light_uped
    with canvas(device) as draw:
        for a in light_uped:
            draw.point((a.get('x'),a.get('y')), fill="black")

    light_uped = []
    current_time = datetime.now().strftime("%H:%M").replace(":", "")
    show_icon(icons.get('clock'))
    show_sign(signs[current_time[0]], [47,48,49,79,80,81,111,112,113,143,144,145,175,176,177])
    show_sign(signs[current_time[1]], [51,52,53,83,84,85,115,116,117,147,148,149,179,180,181])
    show_sign(signs[":"], [87,119,151])
    show_sign(signs[current_time[2]], [57,58,59,89,90,91,121,122,123,153,154,155,185,186,187])
    show_sign(signs[current_time[3]], [61,62,63,93,94,95,125,126,127,157,158,159,189,190,191])

    with canvas(device) as draw:
        for a in light_uped:
            draw.point((a.get('x'),a.get('y')), fill="white")

# show all necessary information about the mail and clears the device before that
def show_mails():
    global light_uped
    with canvas(device) as draw:
        for a in light_uped:
            draw.point((a.get('x'),a.get('y')), fill="black")

    light_uped = []

    show_icon(icons.get("mail"))
    if len(unread_mails) >= 4:
        show_sign(signs["9"], [61,62,63,93,94,95,125,126,127,157,158,159,189,190,191])
        show_sign(signs["9"], [57,58,59,89,90,91,121,122,123,153,154,155,185,186,187])
        show_sign(signs["9"], [53,54,55,85,86,87,117,118,119,149,150,151,181,182,183])
        show_sign(signs["+"], [81,82,83,113,114,115,145,146,147])
    else:
        if len(unread_mails) >= 1:
            show_sign(signs[unread_mails[-1]], [61,62,63,93,94,95,125,126,127,157,158,159,189,190,191])
        if len(unread_mails) >= 2:
            show_sign(signs[unread_mails[-2]], [57,58,59,89,90,91,121,122,123,153,154,155,185,186,187])
        if len(unread_mails) >= 3:
            show_sign(signs[unread_mails[-3]], [53,54,55,85,86,87,117,118,119,149,150,151,181,182,183])

    with canvas(device) as draw:
        for a in light_uped:
            draw.point((a.get('x'),a.get('y')), fill="white")

# show all necessary information about the weather and clears the device before that
def show_weather():
    global light_uped
    with canvas(device) as draw:
        for a in light_uped:
            draw.point((a.get('x'),a.get('y')), fill="black")

    light_uped = []

    if condition == "800" or condition == "801" or condition == "802":
        show_icon(icons.get("weather-sunny"))
    elif condition[0] == "8":
        show_icon(icons.get("weather-cloudy"))
    elif condition[0] == "5" or condition[0] == 3:
        show_icon(icons.get("weather-rainy"))
    elif condition[0] == "7":
        show_icon(icons.get("weather-atmosphere"))
    elif condition[0] == "6":
        show_icon(icons.get("weather-snow"))
    elif condition[0] == "2":
        show_icon(icons.get("weather-thunderstorm"))


    if len(temp) == 2:
        if temp[0] == "-":
            show_sign(signs[temp[1]], [54,55,56,86,87,88,118,119,120,150,151,152,182,183,184])
            show_sign(signs["-"], [115,116])
        else:
            show_sign(signs[temp[0]], [50,51,52,82,83,84,114,115,116,146,147,148,178,179,180])
            show_sign(signs[temp[1]], [54,55,56,86,87,88,118,119,120,150,151,152,182,183,184])
    elif len(temp) == 1:
        show_sign(signs[temp], [54,55,56,86,87,88,118,119,120,150,151,152,182,183,184])
    elif(len(temp) == 3):
        show_sign(signs["-"], [111,112])
        show_sign(signs[temp[1]], [50,51,52,82,83,84,114,115,116,146,147,148,178,179,180])
        show_sign(signs[temp[2]], [54,55,56,86,87,88,118,119,120,150,151,152,182,183,184])

    show_sign(signs["C"], [61,62,63,93,94,95,125,126,127,157,158,159,189,190,191])
    show_sign(signs["^"], [58,59,90,91])


    with canvas(device) as draw:
        for a in light_uped:
            draw.point((a.get('x'),a.get('y')), fill="white")



device.clear()

try:
    # loop that changes the display the hole time
    while True:
        # always add a tick (exspecting the last one, there the tick is set to 0, so the time will be showen)
        # on start show the time
        if tick == 0:
            show_time()
            tick += 1
        elif tick == 3:
            # use a unused tick to load data from the web, so the display isn't unlighted for a moment
            data = requests.get("http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}&units=metric".format(location[0], location[1], open_weather_map_appid)).json()
            temp = str(int(round(data["main"]["temp"])))
            condition = str(data["weather"][0]["id"])
            tick += 1
        elif tick == 12:
	    if use_mail:
            	# use  a unused tick to load data from IMAP client, so the display isn't unlighted for a moment
            	imap = imaplib.IMAP4_SSL(imap4_ssl)
            	imap.login(mail_username, mail_password)
            	imap.select("INBOX")
            	type, data = imap.uid('search', "UNSEEN")
            	unread_mails = str(len(data[0].split()))

            tick+=1
        elif tick == 9:
            show_weather()
            tick += 1
        elif tick == 14:
            if use_mail and unread_mails != "0":
                show_mails()
                tick+=1
            else:
                tick = 0
        elif tick == 17:
            tick = 0
        else:
            tick += 1

        # sleep a moment (one tick -> one second)
        time.sleep(1)
except KeyboardInterrupt:
    device.clear()

