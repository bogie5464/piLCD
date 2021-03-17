import LCD

pins = {
    "LCD_RS" : 4,
    "LCD_E": 17,
    "LCD_DATA4" : 6,
    "LCD_DATA5" : 13,
    "LCD_DATA6" : 19,
    "LCD_DATA7" : 26
}

lcd = LCD.LCD(pins)
lcd.send_message("Hello World!\nHow are you?")