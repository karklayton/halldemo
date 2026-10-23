import qwiic_i2c
import qwiic_buzzer
import time
import qwiic_serlcd
import sys
import math
import asyncio



async def siren(buzzer):
    LOW_HZ = buzzer.NOTE_DS5    
    HIGH_HZ = buzzer.NOTE_AS6
    
    for cycle in range(2):   
        for note in range(LOW_HZ, HIGH_HZ, 10):
            buzzer.configure(note, 0, buzzer.VOLUME_MAX)
            buzzer.on()
            await asyncio.sleep(.02)
        for note in range(HIGH_HZ, LOW_HZ, -10):
            buzzer.configure(note, 0, buzzer.VOLUME_MAX)
            buzzer.on()
            await asyncio.sleep(.02)
    for cycle in range(10):   
        for note in range(LOW_HZ, HIGH_HZ, 150):
            buzzer.configure(note, 0, buzzer.VOLUME_MAX)
            buzzer.on()
            await asyncio.sleep(.015)
        for note in range(HIGH_HZ, LOW_HZ, -150):
            buzzer.configure(note, 0, buzzer.VOLUME_MAX)
            buzzer.on()
            await asyncio.sleep(.015)
    buzzer.off()
    
async def lights_task(lcd):
    while True:
        lcd.setFastBacklight(255, 0, 0)
        await asyncio.sleep(2)
        lcd.setFastBacklight(0, 0, 255)
        await asyncio.sleep(2)
        
async def text_task(lcd):
    message = [['POLICE!', 0], ['PAWS UP!!', 1]]
    lcd.disableSystemMessages()
    lcd.setContrast(0)
    lcd.clearScreen()
    for line in message:
        word = line[0]
        row = line[1]
        start = int((15 - len(word))/2) #centering text
        lcd.setCursor(start, row)
        lcd.print(word)
    #lcd.clearScreen()        
        

async def run(buzzer, lcd):
    lights = asyncio.create_task(lights_task(lcd))
    text = asyncio.create_task(text_task(lcd))
    
    try:
        await siren(buzzer)
    
    finally:
        lcd.setFastBacklight(0, 0, 0)
        lcd.clearScreen()
        lights.cancel()
        text.cancel()
        buzzer.off()
        




