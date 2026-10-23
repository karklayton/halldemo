import qwiic_i2c
import qwiic_buzzer
import time
import qwiic_serlcd
import sys
import math
import asyncio


# Credit to https://github.com/hibit-dev/buzzer for the following tune



async def song(buzzer):
    
    melody = [ buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_DS4, buzzer.NOTE_F4, buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_DS4,
               buzzer.NOTE_F4, buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_DS4, buzzer.NOTE_F4, buzzer.NOTE_G4, buzzer.NOTE_C4,
               buzzer.NOTE_DS4, buzzer.NOTE_F4, buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_E4, buzzer.NOTE_F4, buzzer.NOTE_G4,
               buzzer.NOTE_C4, buzzer.NOTE_E4, buzzer.NOTE_F4, buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_E4, buzzer.NOTE_F4,
               buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_E4, buzzer.NOTE_F4, buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_DS4,
               buzzer.NOTE_F4, buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_DS4, buzzer.NOTE_F4, buzzer.NOTE_D4, buzzer.NOTE_F4,
               buzzer.NOTE_AS3, buzzer.NOTE_DS4, buzzer.NOTE_D4, buzzer.NOTE_F4, buzzer.NOTE_AS3, buzzer.NOTE_DS4, buzzer.NOTE_D4,
               buzzer.NOTE_C4, buzzer.NOTE_G4, buzzer.NOTE_C4, buzzer.NOTE_DS4, buzzer.NOTE_F4, buzzer.NOTE_G4, buzzer.NOTE_C4,
               buzzer.NOTE_DS4, buzzer.NOTE_F4, buzzer.NOTE_D4, buzzer.NOTE_F4, buzzer.NOTE_AS3, buzzer.NOTE_DS4, buzzer.NOTE_D4,
               buzzer.NOTE_F4, buzzer.NOTE_AS3, buzzer.NOTE_DS4, buzzer.NOTE_D4, buzzer.NOTE_C4, buzzer.NOTE_G4, buzzer.NOTE_C4,
               buzzer.NOTE_DS4, buzzer.NOTE_F4, buzzer.NOTE_G4,  buzzer.NOTE_C4, buzzer.NOTE_DS4, buzzer.NOTE_F4, buzzer.NOTE_D4,
               buzzer.NOTE_F4, buzzer.NOTE_AS3, buzzer.NOTE_D4, buzzer.NOTE_DS4, buzzer.NOTE_D4, buzzer.NOTE_AS3, buzzer.NOTE_C4,
               buzzer.NOTE_C5, buzzer.NOTE_AS4, buzzer.NOTE_C4, buzzer.NOTE_G4, buzzer.NOTE_DS4, buzzer.NOTE_DS4, buzzer.NOTE_F4,
               buzzer.NOTE_G4, buzzer.NOTE_C5, buzzer.NOTE_AS4, buzzer.NOTE_C4, buzzer.NOTE_G4, buzzer.NOTE_DS4, buzzer.NOTE_DS4,
               buzzer.NOTE_D4, buzzer.NOTE_C5, buzzer.NOTE_G4, buzzer.NOTE_GS4, buzzer.NOTE_AS4, buzzer.NOTE_C5, buzzer.NOTE_G4,
               buzzer.NOTE_GS4, buzzer.NOTE_AS4, buzzer.NOTE_C5, buzzer.NOTE_G4, buzzer.NOTE_GS4, buzzer.NOTE_AS4, buzzer.NOTE_C5,
               buzzer.NOTE_G4, buzzer.NOTE_GS4, buzzer.NOTE_AS4, buzzer.NOTE_REST, buzzer.NOTE_GS5, buzzer.NOTE_AS5, buzzer.NOTE_C6,
               buzzer.NOTE_G5, buzzer.NOTE_GS5, buzzer.NOTE_AS5, buzzer.NOTE_C6, buzzer.NOTE_G5, buzzer.NOTE_GS5, buzzer.NOTE_AS5,
               buzzer.NOTE_C6, buzzer.NOTE_G5, buzzer.NOTE_GS5, buzzer.NOTE_AS5 ]  
    
    duration = [ 8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16,
                 16, 4, 4, 16, 16, 4, 4, 16, 16, 1, 4, 4, 16, 16, 4, 4, 16, 16, 1, 4, 4, 16, 16, 4, 4, 16, 16, 1, 4, 4, 16,
                 16, 4, 4, 16, 16, 1, 4, 4, 16, 16, 4, 4, 16, 16, 2, 4, 4, 8, 8, 8, 8, 1, 2, 2, 2, 2, 2, 4, 4, 1, 2, 2, 2, 2,
                 2, 4, 4, 8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16, 16, 4, 16, 16, 8, 8, 16, 16, 8, 16, 16, 16, 8,
                 8, 16, 16 ]
        
    

        
    i = 0
    for n in melody:
        note = n
        length = 1 / duration[i]
        buzzer.configure(note, 0, buzzer.VOLUME_MAX)
        buzzer.on()
        await asyncio.sleep(length)
        buzzer.off()
        await asyncio.sleep(.1)
        i = i + 1
    buzzer.off()
    
    
        
async def text_task(lcd):
    lcd.setFastBacklight(255, 255, 255)
    lcd.setContrast(0)
    song = [
    "Oh my sweet     summer kitten,", 
    "what do you knowof fear?",
    "Fear is for the bath time",
    "when the water  falls",
    "a hundred drops deep",
    "and the vacuum  cleaner comes",
    "howling out of  the closet",
    "Fear is for the long empty bowl",
    "when the kibble hides its face",
    "for hours at a  time, and",
    "little kittens  are born and",
    "live and die allwithout churu",
    "while the toys  go unused and",
    "the vets roam   the halls...",
    
            ]
    
    lcd.disableSystemMessages()
    lcd.setContrast(0)
    lcd.clearScreen()
    for word in song:
        lcd.setCursor(0, 0)
        for ch in word: #interrupts the beeps less
            await asyncio.sleep(.06)
            lcd.print(ch)
        await asyncio.sleep(.7)
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

