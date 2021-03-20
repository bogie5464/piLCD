import RPi.GPIO as gpio
import time
from argparse import Namespace


def insert_cgram(index):
    return str(unichr(index))


class LCD:
    LCD_WIDTH = 16  # LCD Character width
    LCD_LINES = 2   # LCD Character lines
    LCD_CHR = gpio.HIGH
    LCD_CMD = gpio.LOW
    E_PULSE = 0.0005
    E_DELAY = 0.0005
    pins = None
    DDRAM_cmd = 0b10000000

    lines = [
        0x0,
        0x40,
        0x14,
        0x54,
    ]

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
        self.send_byte(0x28, self.LCD_CMD)  # Initialize chip in 4 bit mode
        self.send_byte(0x0C, self.LCD_CMD)  # Display on, Cursor off, Cursor blink off.
        self.send_byte(0x06, self.LCD_CMD)  # Sets entry mode Increment bit high
        self.send_byte(0x01, self.LCD_CMD)  # Clear display, set cursor to first line pos 0
        pass
    
    def send_byte(self, bits, mode):
        gpio.output(self.pins.LCD_RS, mode)
        self.__ground()
        # Sends top nibble
        bits = int(bits)
        if bits & 0x10 == 0x10:
            gpio.output(self.pins.LCD_DATA4, gpio.HIGH)
        if bits & 0x20 == 0x20:
            gpio.output(self.pins.LCD_DATA5, gpio.HIGH)
        if bits & 0x40 == 0x40:
            gpio.output(self.pins.LCD_DATA6, gpio.HIGH)
        if bits & 0x80 == 0x80:
            gpio.output(self.pins.LCD_DATA7, gpio.HIGH)
        self.__send()

        self.__ground()
        # Sends bottom nibble
        if bits & 0x01 == 0x01:
            gpio.output(self.pins.LCD_DATA4, gpio.HIGH)
        if bits & 0x02 == 0x02:
            gpio.output(self.pins.LCD_DATA5, gpio.HIGH)
        if bits & 0x04 == 0x04:
            gpio.output(self.pins.LCD_DATA6, gpio.HIGH)
        if bits & 0x08 == 0x08:
            gpio.output(self.pins.LCD_DATA7, gpio.HIGH)
        self.__send()
    pass
    
    def send_message(self, message):
        line_count = 1
        for i in message:
            if i == '\n':
                if line_count > self.LCD_LINES - 1:
                    raise ValueError("Too Many Newlines. " + self.__class__.__name__ + ".LCD_LINES = " +
                                     str(self.LCD_LINES))
                line_count += 1
                self.goto_line(line_count)
            else:
                self.send_byte(ord(i), self.LCD_CHR)
        pass
    
    def create_cgram(self, index, char_data):
        if index > 8 or index < 0:
            raise ValueError("Index must be between 0 and 8")
        index = index * 8
        cgram_cmd = 0b1000000
        cgram_address = cgram_cmd + index
        self.send_byte(cgram_address, self.LCD_CMD)
        for i in char_data:
            self.send_byte(i, self.LCD_CHR)
        first_DDRAM = 0b0010000000
        self.send_byte(first_DDRAM, self.LCD_CMD)

    def print_cgram(self, index):
        self.send_byte(index, self.LCD_CHR)

    def clr(self):
        self.send_byte(0x01, self.LCD_CMD)

    def goto_line(self, linenum):
        if linenum > self.LCD_LINES or linenum < 1:
            raise ValueError("Valid line numbers [1-{}]".format(self.LCD_LINES))

        self.send_byte(self.DDRAM_cmd + self.lines[linenum-1], self.LCD_CMD)

    def goto(self, x, y):
        x = int(x)
        y = int(y)
        if x > self.LCD_LINES:
            raise ValueError("X = " + str(x) + " " + self.__class__.__name__ + ".LCD_LINES = " + str(self.LCD_LINES))

        if y > self.LCD_WIDTH:
            raise ValueError("Y = " + str(y) + " " + self.__class__.__name__ + ".LCD_WIDTH = " + str(self.LCD_WIDTH))

        self.send_byte(self.DDRAM_cmd + self.lines[x-1] + y, self.LCD_CMD)

    def __ground(self):
        # Sets all pins low
        gpio.output(self.pins.LCD_DATA4, gpio.LOW)
        gpio.output(self.pins.LCD_DATA5, gpio.LOW)
        gpio.output(self.pins.LCD_DATA6, gpio.LOW)
        gpio.output(self.pins.LCD_DATA7, gpio.LOW)

    def __send(self):
        time.sleep(self.E_DELAY)
        gpio.output(self.pins.LCD_E, gpio.HIGH)
        time.sleep(self.E_PULSE)
        gpio.output(self.pins.LCD_E, gpio.LOW)
        time.sleep(self.E_DELAY)
