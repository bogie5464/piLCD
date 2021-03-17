import RPi.GPIO as gpio
import time
from argparse import Namespace


class LCD:
    LCD_WIDTH = 16  # LCD Character width
    LCD_LINE_1 = 0x80  # Address of first line
    LCD_LINE_2 = 0xC0  # Address of second line
    LCD_CHR = gpio.HIGH
    LCD_CMD = gpio.LOW
    E_PULSE = 0.0005
    E_DELAY = 0.0005
    pins = None

    def __init__(self, pin_assignment):
        self.pins = Namespace(**pin_assignment)

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.pins.LCD_E, gpio.OUT)
        gpio.setup(self.pins.LCD_RS, gpio.OUT)
        gpio.setup(self.pins.LCD_DATA4, gpio.OUT)
        gpio.setup(self.pins.LCD_DATA5, gpio.OUT)
        gpio.setup(self.pins.LCD_DATA6, gpio.OUT)
        gpio.setup(self.pins.LCD_DATA7, gpio.OUT)
        self.initialize()
        pass
    
    def initialize(self):
        self.send_byte(0x33, self.LCD_CMD)  # Initializes Display in 4 bit mode: Step 1
        self.send_byte(0x32, self.LCD_CMD)  # Initializes Display in 4 bit mode: Step 2
        self.send_byte(0x28, self.LCD_CMD)
        self.send_byte(0x0C, self.LCD_CMD)  # Display on, Cursor off, Cursor blink off.
        self.send_byte(0x06, self.LCD_CMD)  # Sets entry mode Increment bit high
        self.send_byte(0x01, self.LCD_CMD)  # Clear display, set cursor to first line pos 0
        pass
    
    def send_byte(self, bits, mode):
        # Sets all pins low
        gpio.output(self.pins.LCD_RS, mode)
        gpio.output(self.pins.LCD_DATA4, gpio.LOW)
        gpio.output(self.pins.LCD_DATA5, gpio.LOW)
        gpio.output(self.pins.LCD_DATA6, gpio.LOW)
        gpio.output(self.pins.LCD_DATA7, gpio.LOW)
        # Sends top nibble
        if bits & 0x10 == 0x10:
            gpio.output(self.pins.LCD_DATA4, gpio.HIGH)
        if bits & 0x20 == 0x20:
            gpio.output(self.pins.LCD_DATA5, gpio.HIGH)
        if bits & 0x40 == 0x40:
            gpio.output(self.pins.LCD_DATA6, gpio.HIGH)
        if bits & 0x80 == 0x80:
            gpio.output(self.pins.LCD_DATA7, gpio.HIGH)
        time.sleep(self.E_DELAY)
        gpio.output(self.pins.LCD_E, gpio.HIGH)
        time.sleep(self.E_PULSE)
        gpio.output(self.pins.LCD_E, gpio.LOW)
        time.sleep(self.E_DELAY)
        # Sets all pins low
        gpio.output(self.pins.LCD_DATA4, gpio.LOW)
        gpio.output(self.pins.LCD_DATA5, gpio.LOW)
        gpio.output(self.pins.LCD_DATA6, gpio.LOW)
        gpio.output(self.pins.LCD_DATA7, gpio.LOW)
        # Sends bottom nibble
        if bits & 0x01 == 0x01:
            gpio.output(self.pins.LCD_DATA4, gpio.HIGH)
        if bits & 0x02 == 0x02:
            gpio.output(self.pins.LCD_DATA5, gpio.HIGH)
        if bits & 0x04 == 0x04:
            gpio.output(self.pins.LCD_DATA6, gpio.HIGH)
        if bits & 0x08 == 0x08:
            gpio.output(self.pins.LCD_DATA7, gpio.HIGH)
        time.sleep(self.E_DELAY)
        gpio.output(self.pins.LCD_E, gpio.HIGH)
        time.sleep(self.E_PULSE)
        gpio.output(self.pins.LCD_E, gpio.LOW)
        time.sleep(self.E_DELAY)
    pass
    
    def send_message(self, message):
        # message = message.ljust(self.LCD_WIDTH, " ")
        for i in message:
            if i == '\n':
                self.send_byte(0xC0, self.LCD_CMD)
            else:
                self.send_byte(ord(i), self.LCD_CHR)
        pass
    
    def create_cgram(self, index, char_data):
        if index > 8 or index < 0:
            print "Index must be between 0 and 8"
            return
        index = index * 8
        CGRAM_cmd = 0b1000000
        CGRAM_address = CGRAM_cmd + index
        self.send_byte(CGRAM_address, self.LCD_CMD)
        for i in char_data:
            self.send_byte(i, self.LCD_CHR)
        first_DDRAM = 0b0010000000
        self.send_byte(first_DDRAM, self.LCD_CMD)

    def clear_screen(self):
        self.send_byte(0x01, self.LCD_CMD)
