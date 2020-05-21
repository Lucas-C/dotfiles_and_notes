#!/usr/bin/python3

# Trying to see an end to https://ludipe.itch.io/constancia
# INSTALL: pip install keyboard
# USAGE: start this script and immediately focus on your browser window with the game open
#        press CTRL+C to stop it

import keyboard, time

i = 0
while True:
    for key in 'perseverance':
        i += 1
        if i % 121 == 0:
            print(i, key)
        keyboard.press_and_release(key)
        time.sleep(.1)
