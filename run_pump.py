import qwiic_i2c
import qwiic_buzzer
import time
import qwiic_serlcd
import sys
import math
import qwiic_scmd
import asyncio



async def water(pump):
    R_MTR = 0
    L_MTR = 1
    FWD = 0
    BWD = 1
    FLOW_RATE = 140 #gentle stream

    if pump.connected == False:
        print("Motor Driver not connected. Check connections.", file=sys.stderr)
        return
    pump.begin()
    
    # Zero Motor Speeds
    pump.set_drive(0,0,0)
    pump.set_drive(1,0,0)
    
    pump.enable()

    pump.set_drive(R_MTR,FWD,FLOW_RATE)
    await asyncio.sleep(12)
    pump.set_drive(0,0,0)
    
    pump.disable()


async def lights_task(lcd): #gentle white/blue pulse
    while True:
        for i in range(255,100,-10):
            lcd.setFastBacklight(i, i, 255)
            await asyncio.sleep(.1)
        for i in range(100,255,10):
            lcd.setFastBacklight(i, i, 255)
            await asyncio.sleep(.1)
    

async def text_task(lcd): #countdown
    lcd.clearScreen()
    lcd.setContrast(0)
    for i in range(10,0, -1):
        lcd.setCursor(0,0)
        text= f"Dispensing... {i}"
        lcd.print(text)
        await asyncio.sleep(1)
        lcd.clearScreen()
    lcd.setCursor(0,0)
    
    

async def run(buzzer, lcd, pump):
    lights = asyncio.create_task(lights_task(lcd))
    text = asyncio.create_task(text_task(lcd))
    
    try:
        await water(pump)
    
    finally:
        lcd.print("All done! Please come again")
        await asyncio.sleep(1)
        lcd.setFastBacklight(0, 0, 0)
        lcd.clearScreen()
        lights.cancel()
        text.cancel()
        buzzer.off()
        