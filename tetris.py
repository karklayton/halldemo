import qwiic_i2c
import qwiic_buzzer
import time
import qwiic_serlcd
import sys
import math
import asyncio

# Credit to https://github.com/hibit-dev/buzzer for the following tune

async def song(buzzer):
    
    melody= [ buzzer.NOTE_E5, buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_C5, buzzer.NOTE_B4,
        buzzer.NOTE_A4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_E5, buzzer.NOTE_D5, buzzer.NOTE_C5, buzzer.NOTE_B4,
        buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_A4, buzzer.NOTE_A4,
        buzzer.NOTE_B4, buzzer.NOTE_C5,  buzzer.NOTE_D5, buzzer.NOTE_F5, buzzer.NOTE_A5, buzzer.NOTE_G5, 
        buzzer.NOTE_F5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_E5, buzzer.NOTE_D5, buzzer.NOTE_C5, buzzer.NOTE_B4, 
        buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_A4, 
        buzzer.NOTE_REST,   buzzer.NOTE_E5, buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_C5, 
        buzzer.NOTE_B4, buzzer.NOTE_A4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_E5, buzzer.NOTE_D5, buzzer.NOTE_C5,
        buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_A4,
        buzzer.NOTE_A4, buzzer.NOTE_B4, buzzer.NOTE_C5,  buzzer.NOTE_D5, buzzer.NOTE_F5, buzzer.NOTE_A5, 
        buzzer.NOTE_G5, buzzer.NOTE_F5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_E5, buzzer.NOTE_D5, buzzer.NOTE_C5,
        buzzer.NOTE_B4, buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_A4,
        buzzer.NOTE_A4, buzzer.NOTE_REST,
              buzzer.NOTE_E5, buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_C5, buzzer.NOTE_B4,
        buzzer.NOTE_A4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_E5, buzzer.NOTE_D5, buzzer.NOTE_C5, buzzer.NOTE_B4,
        buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_A4, buzzer.NOTE_A4,
        buzzer.NOTE_B4, buzzer.NOTE_C5,  buzzer.NOTE_D5, buzzer.NOTE_F5, buzzer.NOTE_A5, buzzer.NOTE_G5, 
        buzzer.NOTE_F5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_E5, buzzer.NOTE_D5, buzzer.NOTE_C5, buzzer.NOTE_B4, 
        buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_A4, 
#             buzzer.NOTE_REST,  # buzzer.NOTE_E5, buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_C5, 
#             buzzer.NOTE_B4, buzzer.NOTE_A4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_E5, buzzer.NOTE_D5, buzzer.NOTE_C5,
#             buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_A4,
#             buzzer.NOTE_A4, buzzer.NOTE_B4, buzzer.NOTE_C5,  buzzer.NOTE_D5, buzzer.NOTE_F5, buzzer.NOTE_A5, 
#             buzzer.NOTE_G5, buzzer.NOTE_F5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_E5, buzzer.NOTE_D5, buzzer.NOTE_C5,
#             buzzer.NOTE_B4, buzzer.NOTE_B4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_E5, buzzer.NOTE_C5, buzzer.NOTE_A4,
#             buzzer.NOTE_A4, buzzer.NOTE_REST,
              
        ]  

    duration = [ 4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 4, 4, 4, 4, 8, 4, 8, 8,  4, 8, 4, 8, 8, 4, 8, 4, 8,
        8, 4, 8, 8, 4, 4, 4, 4, 4, 4,  4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 4, 4, 4, 4, 8, 4, 8, 8,  4, 8, 4, 8,
        8, 4, 8, 4, 8, 8, 4, 8, 8, 4, 4, 4, 4, 4, 4,
                 4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 4, 4, 4, 4, 8, 4, 8, 8,  4, 8, 4, 8, 8, 4, 8, 4, 8,
        8, 4, 8, 8, 4, 4, 4, 4, 4, 4,  4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 4, 4, 4, 4, 8, 4, 8, 8,  4, 8, 4, 8,
        8, 4, 8, 4, 8, 8, 4, 8, 8, 4, 4, 4, 4, 4, 4,
                 
                 ]
    
    i = 0
    for n in melody:
        note = n
        length = 1 / duration[i]
        buzzer.configure(note, 0, buzzer.VOLUME_MAX)
        buzzer.on()
        await asyncio.sleep(length)
        buzzer.off()
        await asyncio.sleep(.15 * (1- i*.011)) #Speeds up
        i = i + 1
        
    buzzer.off()

def draw_row(lcd, row, cells):
    lcd.setCursor(0, row)
    for n in cells:
        if n == "1":
            lcd._i2c.writeByte(lcd.address, 0x7C, 35)   # custom char slot 0, no delay
        else:
            lcd._i2c.writeCommand(lcd.address, 0x20)    # space
            

async def text_task(lcd):
    WIDTH = 16
    top_row    = "11001100011100000001100011001110001100111000000000110000110000011100000000000011000000110000000011000000111000000000100000000011000000001110000000011"
    bottom_row = "11000110000000111001100110000000001100001000111000110000011000010000001110000011000000011000000011000000000000000011100000000110000000000000000000011"

    lcd.disableSystemMessages()
    lcd.setFastBacklight(255, 255, 255)
    lcd.setContrast(0)
    lcd.clearScreen()
    lcd.specialCommand(0x06)   # left-to-right, no auto-shift

    pad = "0" * WIDTH          # start with an empty screen
    rows = [top_row + pad]
    if bottom_row:
        rows.append(bottom_row + pad)

    # window starts on the empty padding and slides back toward the start of the pattern, so the blocks move left to right
    for start in range(len(rows[0]) - WIDTH, -1, -1):
        for r, strip in enumerate(rows):
            draw_row(lcd, r, strip[start:start + WIDTH])
        await asyncio.sleep(.2)
    


async def run(buzzer, lcd):
    text = asyncio.create_task(text_task(lcd))
    
    try:
        await song(buzzer)
    
    finally:
        lcd.setFastBacklight(0, 0, 0)
        lcd.clearScreen()
        text.cancel()
        buzzer.off()

    
