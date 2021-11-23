from datetime import datetime
from threading import Timer
from inky import InkyPHAT
from flask import Flask, request, jsonify
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from font_fredoka_one import FredokaOne

"""
Service that controlls InkyPhat from a raspberry pi

To test:
curl   'http://192.168.0.244:8899' #writes default message

curl --header 'Content-Type: application/json' \
     -d '{"message": "Hello"}' \
     'http://192.168.0.244:8899/message'

"""
app = Flask("Inky server")
# 212 x 104
ip = InkyPHAT('red')
# ip.set_rotation(180)

daynr = -1

#x = dir(ip)
#print("DIR", x)

weekdays = ("Måndag","Tisdag","Onsdag","Torsdag","Fredag","Lördag","Söndag")
months = ("-", "Jan","Feb","Mars","April","Maj","Juni","Juli", "Aug", "Sept", "Okt", "Nov", "Dec")

# Print centered text at y.
def print_center(text, draw, font, y):
    w, h = font.getsize(text)
    x = int((ip.width - w) / 2)
    draw.text((x, y), text, ip.WHITE, font=font)

def draw_bg(img, ymid):
    for y in range(0, ip.height):
        for x in range(0, ip.width):
            if y < ymid:
                img.putpixel((x, y), ip.RED)
            else:
                img.putpixel((x, y), ip.BLACK)


def print_screen(message = None):
    img = Image.new("P", ip.resolution)
    draw = ImageDraw.Draw(img)

#    hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35))
    top_font = ImageFont.truetype(Intuitive, int(25))
    fredokaOne_font = ImageFont.truetype(FredokaOne, 35)

    # Use system font
    sys_font = ImageFont.truetype('DejaVuSans.ttf', 18)

    td = datetime.today()
    print("M", td.month, td.weekday())
    top_str = f"{weekdays[td.weekday()]} {td.day} {months[td.month]}"

    _, top_h = top_font.getsize(top_str)
    ypadding = 5
    mid = top_h + 2* ypadding
    print (f"Top str size {top_h} padding {ypadding}")

    draw_bg(img, mid)

    bottom_str = "No message"
    bottom_font = fredokaOne_font
    if message:
        if len(message)> 8:
            bottom_font = sys_font
        bottom_str = message

    print_center(top_str, draw, top_font, ypadding)

    print_center(bottom_str, draw, bottom_font, mid + ypadding)

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
        print("New day", day_now)
        daynr = day_now
        print_screen()

    print("Weekday", day_now)

    Timer(60, timer_update).start()


if __name__ == "__main__":
    timer_update()
    app.run(port=8899, host="0.0.0.0")
