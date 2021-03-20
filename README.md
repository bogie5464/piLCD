# piLCD
A library meant to make working with HD44780 LCDs on a raspberry pi a little easier.

Contains 2 pieces. The LCD library, and the Menu Parse library.

The LCD library handles the backend heavy lifting.
- Handles initilization of display
- Supports direct writing of bytes via LCD.send_byte (e.x. LCD.send_byte(0x01, LCD.LCD_CMD) would clear the display)
- Supports sending string of ascii characters with LCD.send_message
- Supports creating cgram via LCD.create_cgram
- Supports printing cgram via LCD.print_cgram
- Supports clearing LCD via LCD.clr()
- Supports loading specific line via LCD.goto_line
- Supports going to arbitrary DDRAM address via LCD.goto

The Menu Parse library handles inline menu generation.
 - Supports execution of any method in the LCD class inline. New feature, possibly buggy. See example for details.
 
Works on displays up to 4 lines.

Currently has no read support, and only supports 4-bit mode, though likely that will change when I get around to the task.
