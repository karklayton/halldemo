import qwiic_i2c
import qwiic_buzzer
import time
import qwiic_serlcd
import sys
import math
import asyncio


# Credit to https://github.com/hibit-dev/buzzer for the following tune

async def song(buzzer):
        
    melody = [ buzzer.NOTE_A4, buzzer.NOTE_REST, buzzer.NOTE_B4, buzzer.NOTE_REST, buzzer.NOTE_C5, buzzer.NOTE_REST, buzzer.NOTE_A4,
               buzzer.NOTE_REST,buzzer.NOTE_D5, buzzer.NOTE_REST, buzzer.NOTE_E5, buzzer.NOTE_REST, buzzer.NOTE_D5, buzzer.NOTE_REST,
               buzzer.NOTE_G4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_E5, buzzer.NOTE_E5, buzzer.NOTE_REST,
               buzzer.NOTE_D5, buzzer.NOTE_REST,buzzer.NOTE_G4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_D5,
               buzzer.NOTE_D5, buzzer.NOTE_REST, buzzer.NOTE_C5, buzzer.NOTE_REST, buzzer.NOTE_B4, buzzer.NOTE_A4, buzzer.NOTE_REST,
               buzzer.NOTE_G4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_REST,
               buzzer.NOTE_B4, buzzer.NOTE_A4, buzzer.NOTE_G4, buzzer.NOTE_REST, buzzer.NOTE_G4, buzzer.NOTE_REST, buzzer.NOTE_D5,
               buzzer.NOTE_REST, buzzer.NOTE_C5, buzzer.NOTE_REST,  buzzer.NOTE_G4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_A4,
               buzzer.NOTE_E5, buzzer.NOTE_E5, buzzer.NOTE_REST, buzzer.NOTE_D5, buzzer.NOTE_REST,  buzzer.NOTE_G4, buzzer.NOTE_A4,
               buzzer.NOTE_C5, buzzer.NOTE_A4, buzzer.NOTE_G5, buzzer.NOTE_B4, buzzer.NOTE_REST, buzzer.NOTE_C5, buzzer.NOTE_REST,
               buzzer.NOTE_B4, buzzer.NOTE_A4, buzzer.NOTE_REST,  buzzer.NOTE_G4, buzzer.NOTE_A4, buzzer.NOTE_C5, buzzer.NOTE_A4,
               buzzer.NOTE_C5, buzzer.NOTE_D5, buzzer.NOTE_REST, buzzer.NOTE_B4, buzzer.NOTE_A4, buzzer.NOTE_G4, buzzer.NOTE_REST,
               buzzer.NOTE_G4, buzzer.NOTE_REST, buzzer.NOTE_D5, buzzer.NOTE_REST, buzzer.NOTE_C5, buzzer.NOTE_REST] #,  buzzer.NOTE_C5,
             #  buzzer.NOTE_REST] #, buzzer.NOTE_D5, buzzer.NOTE_REST, buzzer.NOTE_G4, #buzzer.NOTE_REST, buzzer.NOTE_D5, buzzer.NOTE_REST,
             #  buzzer.NOTE_E5, buzzer.NOTE_REST, buzzer.NOTE_G5, buzzer.NOTE_F5, buzzer.NOTE_E5, buzzer.NOTE_REST,  buzzer.NOTE_C5,
               #buzzer.NOTE_REST, buzzer.NOTE_D5, buzzer.NOTE_REST, buzzer.NOTE_G4, buzzer.NOTE_REST] 

    duration = [
        8, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 2, 8, 8, 2, 8, 8, 8, 8, 8, 2, 8, 8, 4, 8, 8, 8, 8, 8, 8, 8, 8, 2, 8, 8,
        2, 8, 4, 8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 2, 8, 8, 2, 8, 8, 8, 8, 8, 2, 8, 8, 2, 8, 8, 8, 8, 8, 8, 8, 8, 2, 8, 8, 4, 8, 3, 8,
        8, 8, 8, 8, 1, 4, 2, 6, 2, 6, 4, 4, 2, 6, 2, 3, 8, 8, 8, 8, 2, 6, 2, 6, 2, 1]

    i = 0
    for n in melody:
        note = n
        length = 1 / duration[i]
        buzzer.configure(note, 0, buzzer.VOLUME_MAX)
        buzzer.on()
        await asyncio.sleep(length)
        buzzer.off()
        #await asyncio.sleep(.05)
        i = i + 1
    buzzer.off()

    
async def text_task(lcd):
    lcd.setFastBacklight(255, 255, 255)
    song = ["Gotta make you  understand",
    "Never gonna give you up",
            "Never gonna let you down",
            "Never gonna run around",
    "and desert you",
            "Never gonna make you cry",
            "Never gonna say goodbye",
            "Never gonna tell a lie",
    "and hurt you",
            
            ]
    lcd.disableSystemMessages()
    lcd.setContrast(0)
    lcd.clearScreen()
    for word in song:
        start = int((15 - len(word))/2)
        lcd.setCursor(0, 0)
        lcd.print(word)
        await asyncio.sleep(2)
        lcd.clearScreen() 



async def run(buzzer, lcd):
    text = asyncio.create_task(text_task(lcd))
    
    try:
        await song(buzzer)
    
    finally:
        lcd.setFastBacklight(0, 0, 0)
        lcd.clearScreen()
        text.cancel()
        buzzer.off()


