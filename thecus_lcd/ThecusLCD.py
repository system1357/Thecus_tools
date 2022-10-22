import serial
import struct
import platform

class ThecusLCD:
    if platform.system() == 'Windows':
        ser = serial.Serial('COM1', 115200)
    else:
        ser = serial.Serial('/dev/ttyS0', 115200)
    ser.timeout = 10
    ser.writeTimeout = 5
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    command_id_dict = {'SHOW_LCD': b'\x01',
     'CTRL_LCD': b'\x02',
     'EEPROM': b'\x03',
     'BTN_EVENT': b'\x04',
     'VERSION': b'\x05',
     'GPIO': b'\x06',
     'RESET': b'\x07'}
    ctrl_lcd_dict = {'CLEAR': b'\x00',
     'BACKLIGHT_ON': b'\x01',
     'BACKLIGHT_OFF': b'\x02',
     'SET_CURSOR_POS': b'\x03',
     'SET_MSG_POS': b'\x04',
     'SET_CURSOR_TYPE': b'\x05'}
    lcd_width_min = 16
    lcd_width_max = 20

    def write(self, command_id, data):
        """
        @summary: Generate the packet to send to lcm fw
        @param command_id: String
        @param data: String of data
        @return: True for success, False for failure
        """
        schema = [b'\xa0',
         self.command_id_dict[command_id],
         b'\x01',
         b'\x00']
        if data:
            schema[2] = struct.pack('B', len(data))
            schema[3] = data
        final_packet = b''.join(schema)
        try:
            write_count = self.ser.write(final_packet)
            self.ser.flush()
            if write_count > 0:
                return True
        except Exception as e:
            print('Exception: ' + str(e))
            return False

    def read(self):
        """
        @summary: Read the content of the packet
        @return: String, the hex string
        """
        try:
            line = self.ser.read()
            return ''.join(line)
        except:
            return ''

    def readkey(self):
        """
        @summary: Read keys of the lcm display
        @return: Key names(Up, Down, Enter, Esc, unknown)
        """
        key = self.ser.read(4)
        if key == b'\xa1\x04\x02\x01':
            state = 'Down'
        elif key == b'\xa1\x04\x01\x01':
            state = 'Up'
        elif key == b'\xa1\x04\x03\x01':
            state = 'Enter'
        elif key == b'\xa1\x04\x04\x01':
            state = 'Esc'
        elif key == b'':
            state = 'keep_alive'
        else:
            print("Unknown key: ", str(key))
            state = 'unknown'
        return state

    def show_lcd(self, line1, line2):
        """
        @summary: Show the string on the line_1 and line_2 of the lcm display
        @param line1: String.
        @param line2: String.
        @return: True for success, and False for failure
        """
        if line1:
            line_1 = str(line1) + ' ' * self.lcd_width_max
            line_1 = line_1[0:self.lcd_width_min]
            data_1 = self.ctrl_lcd_dict['SET_MSG_POS'] + struct.pack('B', 0) + b'\x00' + line_1.encode()
            self.write('CTRL_LCD', data_1)
        if line2:
            line_2 = str(line2) + ' ' * self.lcd_width_max
            line_2 = line_2[0:self.lcd_width_min]
            data_2 = self.ctrl_lcd_dict['SET_MSG_POS'] + struct.pack('B', 1) + b'\x00' + line_2.encode()
            self.write('CTRL_LCD', data_2)
        return True

    def clear_lcd(self):
        """
        @summary: Clear the screen of the lcm display
        @return: True for success, and False for failure
        """
        self.set_cursor_type(0)
        return self.write('CTRL_LCD', self.ctrl_lcd_dict['CLEAR'])

    def turn_backlight(self, switch):
        """
        @summary: Trun on/off the backlight of the lcm display
        @param switch: 0 = off and 1 = on
        @return: True for success, and False for failure
        """
        if switch not in (0, 1):
            return False
        if switch == 0:
            return self.write('CTRL_LCD', self.ctrl_lcd_dict['BACKLIGHT_OFF'])
        return self.write('CTRL_LCD', self.ctrl_lcd_dict['BACKLIGHT_ON'])

    def set_cursor_position(self, row, column):
        """
        @summary: Set the cursor position on the lcm display
        @param row: Integer in 0 ~ 1
        @param column: Integer in 0 ~ 15
        @return: True for success, and False for failure
        """
        if row not in (0, 1) or column not in range(0, self.lcd_width_min):
            return False
        return self.write('CTRL_LCD', '{0}{1}{2}'.format(self.ctrl_lcd_dict['SET_CURSOR_POS'].decode(), chr(row), chr(column)).encode())

    def set_msg_position(self, row, column, message):
        """
        @summary: Show the message on the indicated position of the lcm display
        @param row: Integer in 0 ~ 1
        @param column: Integer in 0 ~ 15
        @param message: String
        @return: True for success, and False for failure
        """
        if row not in (0, 1) or column not in range(0, self.lcd_width_min):
            return False
        return self.write('CTRL_LCD', '{0}{1}{2}{3}'.format(self.ctrl_lcd_dict['SET_MSG_POS'].decode(), chr(row), chr(column), message).encode())

    def set_cursor_type(self, type):
        """
        @summary: Set the cursor type
        @param type: Integer in 0 ~ 2
        @return: True for success, and False for failure
        """
        if type not in (0, 1, 2):
            return False
        return self.write('CTRL_LCD', '{0}{1}'.format(self.ctrl_lcd_dict['SET_CURSOR_TYPE'].decode(), chr(type)).encode())