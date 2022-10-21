from ThecusLCD import ThecusLCD
from signal import signal, SIGINT
from sys import exit

def handler(signal_received, frame):
    lcd.show_lcd('Thecus NAS', 'Ready')
    print('')
    print('Exit script, GoodBye')
    exit(0)

if __name__ == '__main__':
    signal(SIGINT, handler)
    print('Testing key. Press CTRL-C to exit.')
    print('Press any key on LCD')
    lcd = ThecusLCD()
    lcd.clear_lcd()
    lcd.show_lcd('Testing key', 'Press any key')
    while True:
        read = lcd.readkey()
        print('%s pressed' % (read))
        lcd.show_lcd('Testing key', '%s pressed' % (read))