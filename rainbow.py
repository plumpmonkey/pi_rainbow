import board
import time
import neopixel
import threading

from time import sleep
from flask import Flask, render_template, request
from Mode import *

app = Flask(__name__)

NUM_RED = 11
NUM_ORANGE = 9
NUM_YELLOW = 8
NUM_GREEN = 7
NUM_BLUE = 6
NUM_INDIGO = 5
NUM_VIOLET = 4

RED_START = 0
RED_END = RED_START + NUM_RED - 1
ORANGE_START = RED_END + 1
ORANGE_END = ORANGE_START + NUM_ORANGE -1 
YELLOW_START = ORANGE_END + 1
YELLOW_END = YELLOW_START + NUM_YELLOW -1 
GREEN_START = YELLOW_END + 1
GREEN_END = GREEN_START + NUM_GREEN -1 
BLUE_START = GREEN_END +1
BLUE_END = BLUE_START + NUM_BLUE -1 
INDIGO_START = BLUE_END + 1
INDIGO_END = INDIGO_START + NUM_INDIGO -1
VIOLET_START = INDIGO_END +1
VIOLET_END = VIOLET_START + NUM_VIOLET 

num_pixels = 50
pixels = neopixel.NeoPixel(board.D18, num_pixels, brightness=0.6, auto_write=False)

ORDER = neopixel.GRB
mode = Mode.UNKNOWN

pixels.show()

@app.route('/', methods = ['POST', 'GET'])
def home_page():

    global mode

    if request.method == 'POST':

        action = request.form['control'];

        if( "cycle" in action):            
            mode = Mode.CYCLE
        elif ("rider" in action):
            mode = Mode.RIDER
        elif ("rainbow" in action):
            mode = Mode.RAINBOW
        elif("off" in action):
            mode = Mode.OFF
        else:
            mode = Mode.UNKNOWN

    return render_template('index.html')


@app.route('/button/<name>')
def hello_world(name):
    return 'Hello %s!' % name


@app.before_first_request
def initialize():
    # Called only once, when the first request comes in

    activity_thread = threading.Thread(target=activity_loop, daemon=True)
    activity_thread.start()


def activity_loop():
    global mode

    while(True):
        if mode == Mode.CYCLE:
            cycle_led(0.01)
        elif mode == Mode.OFF:
            clearStrip()
        elif mode == Mode.RIDER:
            rider()
        elif mode == Mode.RAINBOW:
            rainbow(0.1, 1)
        elif mode == Mode.PAUSE:
            sleep(2)


def red_on(inter_light_delay):

    for i in range(RED_START,ORANGE_START):
        pixels[i] = (0, 255, 0)
        if( inter_light_delay != 0):
            pixels.show()
            sleep(inter_light_delay)

    if(inter_light_delay == 0):
        pixels.show()

def orange_on(inter_light_delay):

    for i in range(ORANGE_START, YELLOW_START):
        pixels[i] = (165, 255, 0)
        if( inter_light_delay != 0):
            pixels.show()
            sleep(inter_light_delay)

    if(inter_light_delay == 0):
        pixels.show()


def yellow_on(inter_light_delay):

    for i in range(YELLOW_START,GREEN_START):
        pixels[i] = (255, 255, 0)
        if( inter_light_delay != 0):
            pixels.show()
            sleep(inter_light_delay)

    if(inter_light_delay == 0):
        pixels.show()


def green_on(inter_light_delay):

    for i in range(GREEN_START,BLUE_START):
        pixels[i] = (255, 0, 0)
        if( inter_light_delay != 0):
            pixels.show()
            sleep(inter_light_delay)

    if(inter_light_delay == 0):
        pixels.show()

def blue_on(inter_light_delay):

    for i in range(BLUE_START,INDIGO_START):
        pixels[i] = (0, 0, 255)
        if( inter_light_delay != 0):
            pixels.show()
            sleep(inter_light_delay)

    if(inter_light_delay == 0):
        pixels.show()

def indigo_on(inter_light_delay):

    for i in range(INDIGO_START,VIOLET_START):
        pixels[i] = (0, 75, 160)
        if( inter_light_delay != 0):
            pixels.show()
            sleep(inter_light_delay)

    if(inter_light_delay == 0):
        pixels.show()


def violet_on(inter_light_delay):

    for i in range(VIOLET_START,VIOLET_END):
        pixels[i] = (130, 238, 238)
        if( inter_light_delay != 0):
            pixels.show()
            sleep(inter_light_delay)

    if(inter_light_delay == 0):
        pixels.show()


def all_on(inter_light_delay = 0, inter_colour_delay=0):

    red_on(inter_light_delay)
    sleep(inter_colour_delay)

    orange_on(inter_light_delay)
    sleep(inter_colour_delay)

    yellow_on(inter_light_delay)
    sleep(inter_colour_delay)

    green_on(inter_light_delay)
    sleep(inter_colour_delay)

    blue_on(inter_light_delay)
    sleep(inter_colour_delay)

    indigo_on(inter_light_delay)
    sleep(inter_colour_delay)

    violet_on(inter_light_delay)
    sleep(inter_colour_delay)

def flash_all(on_delay, off_delay, loops):
    
    for i in range(0,loops):
        all_on(0)
        sleep(on_delay)
        clearStrip()
        sleep(off_delay)

def middle_out(inter_group_delay = 1):
    green_on(0)
    sleep(inter_group_delay)

    yellow_on(0)
    blue_on(0)
    sleep(inter_group_delay)

    orange_on(0)
    indigo_on(0)
    sleep(inter_group_delay)

    red_on(0)
    violet_on(0)
    sleep(2)

    clearStrip()

def outside_in(inter_group_delay = 1):

    red_on(0)
    violet_on(0)
    sleep(inter_group_delay)

    orange_on(0)
    indigo_on(0)
    sleep(inter_group_delay)

    yellow_on(0)
    blue_on(0)
    sleep(inter_group_delay)

    green_on(0)
    sleep(2)

    clearStrip()


def slow_on():
    all_on(inter_light_delay = 0.1, inter_colour_delay=0)
    sleep(2)
    clearStrip()

def slow_flash():
    flash_all(on_delay=1.5, off_delay=1, loops=6)
    clearStrip()

def quick_flash():
    flash_all(on_delay=0.05, off_delay=0.05, loops=40)
    clearStrip()

def sections_on():
    all_on(0, 0.7)
    sleep(2)
    clearStrip()
def rainbow(inter_colour_delay, inter_light_delay):

    clearStrip()

    middle_out()

    slow_on()

    slow_flash()

    sections_on()

    slow_flash()

    outside_in()
    
    quick_flash()


def rider():
    pos = 5
    direction = 1

    while mode == Mode.RIDER:

        pixels[pos - 5] = (0, 16, 0)
        pixels[pos - 4] = (0, 46, 0)
        pixels[pos - 3] = (0, 96, 0)
        pixels[pos - 2] = (0, 128, 0)
        pixels[pos - 1] = (0,255, 0)
        pixels[pos] = (0, 255, 0)
        if (pos+5 < num_pixels - 5):
            pixels[pos + 1] = (0, 255, 0)
            pixels[pos + 2] = (0, 128, 0)
            pixels[pos + 3] = (0, 96, 0)
            pixels[pos + 4] = (0, 46, 0)
            pixels[pos + 5] = (0, 16, 0)

        pixels.show()

        time.sleep(0.03)

        clearStrip()
        
        pos += direction
        
        if pos < 5:
            pos = 5
            direction = -direction
        elif pos >= (num_pixels ):
            pos = num_pixels - 1
            direction = -direction


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def cycle_led(wait):
    global mode
    global pixels

    print("Cycle LED")
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)

        pixels.show()
        time.sleep(wait)

def clearStrip():
    pixels.fill((0, 0, 0))
    pixels.show()
    

def stop_led():
    
    global pixels
    global mode

    print("Stop LED")
    clearStrip()

    mode = Mode.PAUSE


if __name__ == '__main__':
    app.run(debug=True, port='80', host='0.0.0.0')
