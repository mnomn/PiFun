from datetime import datetime
from threading import Timer
from inky import InkyPHAT
from flask import Flask, request, jsonify
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from font_fredoka_one import FredokaOne
import os
import logging

import arguments
from weather import *
from settings import *

"""
Service that controlls InkyPhat from a raspberry pi

To test:
curl   'http://192.168.0.244:8899' #writes default message

curl --header 'Content-Type: application/json' \
     -d '{"message": "Hello"}' \
     'http://192.168.0.244:8899/message'

"""

settings = Settings()
weather = Weather(settings.get(Settings.CITY), settings.get(Settings.API_KEY))
log = logging.getLogger("inkCal")

app = Flask("Inky server")
# 212 x 104
ip = InkyPHAT('red')

#ip.set_rotation(x) in later versions
if settings.get(Settings.ROTATION):
    ip.h_flip = True
    ip.v_flip = True

daynr = -1

weekdays = ("Måndag","Tisdag","Onsdag","Torsdag","Fredag","Lördag","Söndag")
#weekdays = ("Mån","Tis","Ons","Tor","Fre","Lör","Sön")
months = ("-", "jan","feb","mars","april","maj","juni","juli", "aug", "sept", "okt", "nov", "dec")

PATH = os.path.dirname(__file__)

# Print centered text at y.
def print_center(text, draw, font, y, color = ip.WHITE):
    w, h = font.getsize(text)
    x = int((ip.width - w) / 2)
    draw.text((x, y), text, color, font=font)

def draw_bg(img, ymid):
    for y in range(0, ip.height):
        for x in range(0, ip.width):
            if y < ymid:
                img.putpixel((x, y), ip.RED)
            else:
                img.putpixel((x, y), ip.BLACK)

def create_mask(source, mask=(ip.WHITE, ip.BLACK, ip.RED)):
    """Create a transparency mask.
    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.
    :param mask: Optional list of Inky pHAT colours to allow.
    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image

def print_screen(message = None):
#    ip.set_rotation(rotation)
    img = Image.new("P", ip.resolution)
    draw = ImageDraw.Draw(img)

#    hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35))
    top_font = ImageFont.truetype(Intuitive, int(20))
    fredokaOne_font = ImageFont.truetype(FredokaOne, 30)

    # Use system font
    sys_font = ImageFont.truetype('DejaVuSans.ttf', 18)


    td = datetime.today()
    log.info(f"Weekday {td.weekday()} Month: {td.month}")

    iso_cal = td.isocalendar()
    log.info(f"Week no {iso_cal.week}")

    top_str = f"{weekdays[td.weekday()]} {td.day} {months[td.month]} v{iso_cal.week}"

    _, top_h = top_font.getsize(top_str)
    ypadding = 5
    mid = top_h + 2* ypadding

    top_text_pos = ypadding
    mid_text_pos = mid + ypadding
    bottom_text_pos = ip.height - top_h - 2* ypadding

    log.info(f"String at (y) {top_text_pos} padding {mid_text_pos}, bottom {bottom_text_pos}")

    draw_bg(img, mid)

#    bottom_font = fredokaOne_font
    bottom_font = sys_font

    if not message:
        log.info("No message, get weather")
        message = ""

    weather_ico = weather.getIcon()

    if weather_ico:
        img_path = os.path.join(PATH, "icons", weather_ico)
        log.info(f"use icon {img_path}")
        icon_image = Image.open(img_path)
        icon_mask = create_mask(icon_image)
        img.paste(icon_image, (8, 60), icon_mask)
    else:
        log.info(f"No icon found")

    print_center(top_str, draw, top_font, top_text_pos)
    if message:
        print_center(message, draw, bottom_font, mid_text_pos)
    print_center(weather.getString(), draw, bottom_font, bottom_text_pos)

    ip.set_image(img)
    ip.show()


@app.route("/")
def route_root():
    print_screen()
    return f"Hej hej {datetime.today()}"

@app.post("/message")
def route_message():
    content = request.json
    message = content.get('message', None)
    print_screen(message)
    return jsonify({"updated":datetime.today()})


def timer_update():
    global daynr
    day_now = datetime.today().weekday()
    if day_now != daynr:
        log.info(f"New day {day_now}")
        daynr = day_now
        print_screen()

    log.info(f"Weekday {day_now}")

    Timer(60, timer_update).start()


def init():
    args = arguments.get()
    logging.basicConfig(level=args.log.upper())

#     log.setLevel(level=args.log.upper())
    log.info("Starting service")
    log.warning("Starting service W")

if __name__ == "__main__":
    init()
    timer_update()
    app.run(port=8899, host="0.0.0.0")
