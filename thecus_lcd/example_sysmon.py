from time import sleep
from ThecusLCD import ThecusLCD
from signal import signal, SIGINT
from sys import exit
from threading import Timer
import time
import os
import socket
import re

menuloc = 0
menuloc2 = 0
escstat = False
cmdlock = False
testmode = False
bltimer = 0

menu_items = {0: 'Tog. Backlight',
    1: 'Tog. fan speed',
    2: 'Tog. HDD LED',
    3: 'Tog. USB GRNLED',
    4: 'Tog. USB REDLED'}

def handler(signal_received, frame):
    t.cancel()
    lcd.turn_backlight(1)
    lcd.show_lcd('Thecus NAS', 'Ready')
    print('')
    print('Exit script, GoodBye')
    exit(0)

def backlight_ctrl():
    global t, bltimer
    bltimer += 1
    if bltimer <= 3:
        t = Timer(1, backlight_ctrl)
        t.start()
    if bltimer > 3:
        bltimer = 0
        lcd.turn_backlight(0)
        t = Timer(1, backlight_ctrl)
        t.start()

def menuloop(key):
    global menuloc
    if key == 'Up':
        if menuloc > 0:
            menuloc -= 1
        else:
            menuloc = 4
    if key == 'Down':
        if menuloc == 4:
            menuloc = 0
        else:
            menuloc += 1
    return menu_items[menuloc]

def menuloop2(key):
    global menuloc2
    if key == 'Up':
        if menuloc2 > 0:
            menuloc2 -= 1
        else:
            menuloc2 = 6
    if key == 'Down':
        if menuloc2 == 6:
            menuloc2 = 0
        else:
            menuloc2 += 1
    menu2_parse(menuloc2)

def menu2_parse(key):
    hostname = socket.gethostname()
    IPAddr :str = socket.gethostbyname(hostname)
    if key == 0:
        lcd.show_lcd('Thecus NAS', 'Ready')
    if key == 1:
        lcd.show_lcd('Thecus NAS', 'IP: %s' % IPAddr)
    if key == 2:
        lcd.show_lcd('Thecus NAS', 'Hostname: %s' % hostname)
    if key == 3:
        update_lcdval('CPU')
    if key == 4:
        update_lcdval('SAS')
    if key == 5:
        update_lcdval('FAN')
    if key == 6:
        lcd.show_lcd('Thecus NAS', 'TEST Mode')

def update_lcdval(name):
    fp = open('/proc/hwm', 'r')
    for line in fp:
        if re.search(name, line):
            line2 = line.strip()
    fp.close()
    lcd.show_lcd('Thecus NAS', line2)

def runfunc(num):
    global cmdlock
    try:
        cmdlock = True
        lcd.show_lcd('Testing LCM & HW', 'In Progress...')
        if num == 0:
            lcd.turn_backlight(0)
            sleep(3)
            lcd.turn_backlight(1)
        if num == 1:
            os.system('echo "REG 1 0x6b 0xFF" > /proc/hwm')
            sleep(5)
            os.system('echo "REG 1 0x6b 0x35" > /proc/hwm')
        if num == 2:
            os.system('gpioset 1 0=0')
            sleep(1)
            os.system('gpioset 1 3=0')
            sleep(1)
            os.system('gpioset 1 7=0')
            sleep(1)
            os.system('gpioset 1 1=0')
            sleep(1)
            os.system('gpioset 1 0=1')
            sleep(1)
            os.system('gpioset 1 3=1')
            sleep(1)
            os.system('gpioset 1 7=1')
            sleep(1)
            os.system('gpioset 1 1=1')
            sleep(1)
        if num == 3:
            os.system('gpioset 1 8=0')
            sleep(1)
            os.system('gpioset 1 8=1')
        if num == 4:
            os.system('gpioset 1 6=0')
            sleep(1)
            os.system('gpioset 1 6=1')
        cmdlock = False
        lcd.show_lcd('Testing LCM & HW', menu_items[menuloc])
        return True
    except Exception as e:
        print('Exception: ' + str(e))
        cmdlock = False
        return False

if __name__ == '__main__':
    signal(SIGINT, handler)
    print('Thecus Monitor. Press CTRL-C to exit.')
    lcd = ThecusLCD()
    lcd.clear_lcd()
    lcd.show_lcd('Thecus NAS', 'Ready')
    lcd.turn_backlight(1)
    os.system('echo "SLED 2 0 1" > /proc/hwm')
    t = Timer(1, backlight_ctrl)
    t.start()
    while True:
        read = lcd.readkey()
        if read == 'Enter':
            bltimer = 0
            lcd.turn_backlight(1)
            if menuloc2 == 6 and escstat == False and cmdlock == False and testmode == False:
                testmode = True
                escstat = False
                cmdlock = False
                lcd.show_lcd('Testing LCM & HW', 'Tog. Backlight')
            elif escstat == False and cmdlock == False and testmode == True:
                t.cancel()
                runfunc(menuloc)
                t = Timer(1, backlight_ctrl)
                t.start()
            elif escstat == True and cmdlock == False:
                lcd.show_lcd('Thecus NAS', 'Ready')
                testmode = False
                escstat = False
                cmdlock = False
        elif read == 'Esc':
            bltimer = 0
            lcd.turn_backlight(1)
            if escstat == False and testmode == True:
                escstat = True
                lcd.show_lcd('Testing LCM & HW', 'Quit Test?')
            elif escstat == True and testmode == True:
                escstat = False
                lcd.show_lcd('Testing LCM & HW', menuloop(read))
        elif read == 'Up' or read == 'Down':
            bltimer = 0
            lcd.turn_backlight(1)
            if testmode == True:
                lcd.show_lcd('Testing LCM & HW', menuloop(read))
            else:
                menuloop2(read)
        else:
            pass