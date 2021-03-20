import LCD
import MenuParse

pins = {
    "LCD_RS" : 4,
    "LCD_E": 17,
    "LCD_DATA4" : 6,
    "LCD_DATA5" : 13,
    "LCD_DATA6" : 19,
    "LCD_DATA7" : 26
}

Bell = 0x04, 0x0E, 0x0E, 0x0E, 0x1F, 0x04, 0x00, 0x00

lcd = LCD.LCD(pins)
lcd.LCD_WIDTH = 20
lcd.LCD_LINES = 4
lcd.create_cgram(0, Bell)

menu_entry = r"For whom the {print_cgram:0} tolls{goto:3, 0}Hello world!"
menu = MenuParse.LCD_Menu(lcd, message=menu_entry)
menu.parse()