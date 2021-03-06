import board
import neopixel
import pytz
import random
import threading
import time

from time import sleep
from datetime import datetime
from flask import Flask, render_template, request
from Mode import *

last_pattern = 99 # Used to prevent the same pattern being selected twice

app = Flask(__name__)

# Define the number of LEDs in each colour segment
NUM_RED = 10
NUM_ORANGE = 10
NUM_YELLOW = 8
NUM_GREEN = 7
NUM_BLUE = 6
NUM_INDIGO = 5
NUM_VIOLET = 4

# Work out start and end LEDs
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

# Number of pixels in the string
num_pixels = 50
pixels = neopixel.NeoPixel(board.D18, num_pixels, brightness=0.6, auto_write=False)

ORDER = neopixel.GRB
mode = Mode.UNKNOWN

pixels.show()

#################################################################################
#
# Flask functions
#
#################################################################################
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
        elif ("clap" in action):
            mode = Mode.CLAP
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

#################################################################################
#
# LED functions
#
#################################################################################

# Main thread. Checks for mode change every two seconds
def activity_loop():
    global mode

    while(True):
        if mode == Mode.CYCLE:
            # Cycles the led colurs through the rainbow and string
            cycle_led(0.01)

        elif mode == Mode.OFF:
            # Switch lights off
            clearStrip()

        elif mode == Mode.RIDER:
            # Knight Rider init!
            rider()

        elif mode == Mode.RAINBOW:
            # NHS Rainbow mode
            rainbow()
            
        elif mode == Mode.PAUSE:
            # After lights have been switched off, sleep for 2 seconds
            # before checking for a new mode. Prevents hammering the
            # code.
            sleep(2)

        elif mode == Mode.CLAP:
            # Test mode to test the 8pm clap
            thursdayClap(delay=0.2, loops=1)


#
# Utility functions to switch the individual colour light sections
# on.
#
# inter_light_delay - delay between switching on each light of the
#                     same colour. If no delay, then slightly kooky
#                     code prevents a perceptable delay which is introduced
#                     by calling pixels.show() for each light
#
def all_white():
    
    pixels.fill((255,255,255))
    pixels.show()
    
    
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

        
#
# Switch all the colours on.
#
# inter_light_delay  - delay between LEDs of same colour
# inter_colour_delay - delay between different colour segments
#
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

#
# Patterns
#

#
# Flash all the lights
#
# on_delay  - time lights are on
# off_delay - time lights are off
# loops     - number of flashes
#
def flash_all(on_delay, off_delay, loops):
    
    for i in range(0,loops):
        clearStrip()
        sleep(off_delay)
        all_on(0)
        sleep(on_delay)

#
# Middle Out. Enable via segments. 1) green
# 2) yellow+blue, 3) orange/indigo, 4) red/violet
#
# inter_group_delay - Time delay between enabling segments
#
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

    
#
# Outside In. Enable via segments. 1) red/violet
# 2) orange/indigo, 3) yellow/blue, 4) green
#
# inter_group_delay - Time delay between enabling segments
#
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


#
# Slow On - Enable each light in turn along the string,
# starting with red.
#
# inter_light_delay  - delay between LEDs of same colour
# inter_colour_delay - delay between different colour segments
# 
def slow_on():
    all_on(inter_light_delay = 0.1, inter_colour_delay=0)
    sleep(2)
    clearStrip()


#
# Slow flash - Flash all the LEDs slowly
#
# on_delay  - time lights are on
# off_delay - time lights are off
# loops     - number of flashes
# 
def slow_flash():
    flash_all(on_delay=1.5, off_delay=1, loops=6)
    clearStrip()

#
# Quick flash - Flash all the LEDs quickly
#
# on_delay  - time lights are on
# off_delay - time lights are off
# loops     - number of flashes
# 
def quick_flash():
    flash_all(on_delay=0.02, off_delay=0.02, loops=40)
    clearStrip()

def quick_flash_white(loops=40, off_delay=0.02, on_delay=0.02):
    for i in range(0,loops):
        clearStrip()
        sleep(off_delay)
        all_white()
        sleep(on_delay)

    clearStrip()


#
# Sections on - Enable the lights section by section
# starting with red.
#
def sections_on():
    all_on(0, 0.7)
    sleep(2)
    clearStrip()


#
# Rotate through all sections, only one section is lit
# at any time. Start with Red
# 
def individual_sections():

    delay = 0.75

    red_on(0)
    sleep(delay)
    clearStrip()

    orange_on(0)
    sleep(delay)
    clearStrip()

    yellow_on(0)
    sleep(delay)
    clearStrip()

    green_on(0)
    sleep(delay)
    clearStrip()

    blue_on(0)
    sleep(delay)
    clearStrip()

    indigo_on(0)
    sleep(delay)
    clearStrip()

    violet_on(0)
    sleep(delay)
    clearStrip()


#
# Rotate through all sections, only one section is lit
# at any time. Start with violet
# 
def reverse_individual_sections():

    delay = 0.75

    violet_on(0)
    sleep(delay)
    clearStrip()

    indigo_on(0)
    sleep(delay)
    clearStrip()

    blue_on(0)
    sleep(delay)
    clearStrip()

    green_on(0)
    sleep(delay)
    clearStrip()

    yellow_on(0)
    sleep(delay)
    clearStrip()

    orange_on(0)
    sleep(delay)
    clearStrip()

    red_on(0)
    sleep(delay)
    clearStrip()


#
# Random Segment. Pick a random segment, enable it,
# disable it, repeat for X number of segments
# 
def random_segment():

    loops = 10
    delay_on = 1.0
    delay_off = 0.2
    last_segment = 99

    clearStrip()

    segment = last_segment
    
    for x in range(loops):

        while(segment == last_segment):
            segment = random.randint(0,6)

        last_segment = segment
        
        if segment == 0:
            red_on(0)
        elif segment == 1:
            orange_on(0)
        elif segment == 2:
            yellow_on(0)
        elif segment == 3:
            green_on(0)
        elif segment == 4:
            blue_on(0)
        elif segment == 5:
            indigo_on(0)
        elif segment == 6:
            violet_on(0)
        else:
            print("Invalid random_segment! {} ".format(segment))

        sleep(delay_on)
        clearStrip()
        sleep(delay_off)

#
# Thursday Clap!
#
# For one minute, flash the lights randomly.
#
def thursdayClap(delay=0.2, loops = 1):

    for k in range(0,loops):
        for i in range(0, num_pixels):
            # Pick a random colour
            colour = random.randint(0,6)
            if(colour == 0):
                pixels[i] = (0,255,0)

            elif(colour == 1):
                pixels[i] = (165,255,0)

            elif(colour == 2):
                pixels[i] = (255,255,0)

            elif(colour == 3):
                pixels[i] = (255,0,0)

            elif(colour == 4):
                pixels[i] = (0,0,255)

            elif(colour == 5):
                pixels[i] = (0,75,160)

            elif(colour == 6):
                pixels[i] = (130,238,238)

            pixels.show()
            sleep(delay)
    

#
# Main rainbow routine.
#
# Select one of the routines by random to execute
#
def rainbow():

    global last_pattern

    # Check for Thursday 8pm
    tz = pytz.timezone('Europe/London')
    
    weekday = datetime.today().weekday()
    time = datetime.now(tz).strftime("%H%M")
    if weekday == 3 and time == "2000":
        thursdayClap(0.05)
    else:
    
        pattern = last_pattern
    
        # Select a new pattern. ensure its not the
        # same as the last one we executed
        while (pattern == last_pattern):
            pattern = random.randint(0,9)

            last_pattern = pattern
    
            clearStrip()

            if pattern == 0:
                random_segment()
            elif pattern == 1:
                individual_sections()
            elif pattern == 2:
                reverse_individual_sections()
                quick_flash_white()
            elif pattern == 3:
                middle_out()
            elif pattern == 4:
                slow_on()
            elif pattern == 5:
                sections_on()
            elif pattern == 6:
                slow_flash()
            elif pattern == 7:
                outside_in()
            elif pattern == 8:
                quick_flash()
            elif pattern == 9:
                thursdayClap(delay = 0.2, loops = 40)
        else:
            print("Invalid pattern! {}".format(pattern))


#
# Knight rider mode
#
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


#
# Used for colour cycle
#
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

#
# Cycle the LEDs
#
def cycle_led(wait):
    global mode
    global pixels

    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)

        pixels.show()
        time.sleep(wait)

        
#
# Turn off all lights
#
def clearStrip():
    pixels.fill((0, 0, 0))
    pixels.show()
    

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

