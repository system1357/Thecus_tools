from time import sleep
from ThecusLCD import ThecusLCD
from signal import signal, SIGINT
from sys import exit
import os

menuloc = 0
escstat = False
cmdlock = False
menu_items = {0: 'Tog. Backlight',
    1: 'Tog. fan speed',
    2: 'Tog. HDD LED',
    3: 'Tog. USB GRNLED',
    4: 'Tog. USB REDLED'}

def handler(signal_received, frame):
    lcd.show_lcd('Thecus NAS', 'Ready')
    print('')
    print('Exit script, GoodBye')
    exit(0)

def menuloop(key):
    global menuloc
    if key == 'Up':
        if menuloc > 0:
            menuloc -= 1
        else:
            menuloc = 0
    if key == 'Down':
        if menuloc == 4:
            pass
        else:
            menuloc += 1
    return menu_items[menuloc]

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

def handlebtn(btn):
    print(btn)
    if btn == 'Enter':
            runfunc(menuloc)
            print(btn)
    elif btn == 'Esc':
        lcd.show_lcd('Testing LCM & HW', 'Quit Test?')
        if btn == 'Enter':
            lcd.show_lcd('Thecus NAS', 'Ready')
            print('Exit script, GoodBye')
            exit(0)
        elif btn == 'Esc':
            lcd.show_lcd('Testing LCM & HW', menuloop(btn))
    else:
        lcd.show_lcd('Testing LCM & HW', menuloop(btn))

if __name__ == '__main__':
    signal(SIGINT, handler)
    print('Testing LCM & HW. Press CTRL-C to exit.')
    print('Press any key on LCD')
    lcd = ThecusLCD()
    lcd.clear_lcd()
    lcd.show_lcd('Testing LCM & HW', 'Tog. Backlight')
    while True:
        read = lcd.readkey()
        if read == 'Enter':
            if escstat == False and cmdlock == False:
                runfunc(menuloc)
            if escstat == True and cmdlock == False:
                lcd.show_lcd('Thecus NAS', 'Ready')
                print('Exit script, GoodBye')
                exit(0)
        elif read == 'Esc':
            if escstat == False:
                escstat = True
                lcd.show_lcd('Testing LCM & HW', 'Quit Test?')
            elif escstat == True:
                escstat = False
                lcd.show_lcd('Testing LCM & HW', menuloop(read))
        else:
            lcd.show_lcd('Testing LCM & HW', menuloop(read))