import qwiic_i2c
import BLE
import qwiic_buzzer
import time
import qwiic_serlcd
import sys
from TMAG5273 import HallSensor, TMAG_ADDR_PRIMARY
import math
import qwiic_scmd
import asyncio
import police
import got
import never
import tetris
import run_pump

 
# SparkFun Thing Plus ESP32 WROOM: Qwiic connector = SDA GPIO21, SCL GPIO22
my_bus = qwiic_i2c.get_i2c_driver(sda=21, scl=22, freq=100000)


 
scan_list = my_bus.scan()
print("Bus scan:", [hex(a) for a in scan_list])
 
if scan_list:
    device_address = scan_list[0]
    print("Device", hex(device_address), "connected:", my_bus.ping(device_address))
else:
    print("No I2C devices found, check wiring")

pump = qwiic_scmd.QwiicScmd()
buzzer = qwiic_buzzer.QwiicBuzzer()

# Hall sensor shares the same bus (do not let it create its own on other pins)
hall_sensor = None
if TMAG_ADDR_PRIMARY in scan_list:
    hall_sensor = HallSensor(scl_pin=22, sda_pin=21, addr=TMAG_ADDR_PRIMARY,
                             i2c=my_bus._i2cbus)
else:
    print("TMAG5273 not found at", hex(TMAG_ADDR_PRIMARY), "- check the scan list above")

lcd = qwiic_serlcd.QwiicSerlcd()
if lcd.connected == False:
    print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", file=sys.stderr)

modes = ["pump", "got", "police", "never", "tetris", ]


# detects change in magnetic field
def field_watch(mode):
    threshold = BLE.sensitivity
    
    print("threshold " + str(threshold) + "\n")
    
    if hall_sensor is None:
        print("No hall sensor")
        return

    n = 20 # 20 sample average
    bx = by = bz = 0.0
    
    for _ in range(n):
        bx += hall_sensor.get_mag_x()
        by += hall_sensor.get_mag_y()
        bz += hall_sensor.get_mag_z()
        time.sleep(0.05)
    bx /= n
    by /= n
    bz /= n
    print("Baseline: X %.3f  Y %.3f  Z %.3f mT" % (bx, by, bz))

    x = y = z = 0
    
    while True:
        
        for _ in range(n):
            x += hall_sensor.get_mag_x()
            y += hall_sensor.get_mag_y()
            z += hall_sensor.get_mag_z()
            time.sleep(0.05)
        x /= n
        y /= n
        z /= n
        
        delta = math.sqrt((x - bx) ** 2 + (y - by) ** 2 + (z - bz) ** 2)
        
        if delta > threshold:

            
            print("FIELD CHANGE  delta = %.3f mT" % delta)
            
            
            check_thresh = float(BLE.sensitivity)
            
            if float(threshold) != check_thresh:
                threshold = check_thresh
                BLE.send("Triggered " + str(threshold))
                print("threshold " + str(threshold) + "\n")
                continue
            
            mode = BLE.mode
            BLE.send("Triggered " + mode)
            
            if mode in modes: 
                if mode == "pump":
                    asyncio.run(run_pump.run(buzzer, lcd, pump))
                elif mode == "police":
                    asyncio.run(police.run(buzzer, lcd))
                elif mode == "got":
                    asyncio.run(got.run(buzzer, lcd))
                elif mode == "never":
                    asyncio.run(never.run(buzzer, lcd))
                elif mode == "tetris":
                    asyncio.run(tetris.run(buzzer, lcd))
                else:
                    print("something has gone horribly wrong")    
            else:
                BLE.send("not a valid mode, choose pump, got, police, never, or tetris")
       
            time.sleep(1)

        elif delta < threshold:
            #print("threshold " + str(threshold))
            print("NORMAL  delta = %.3f mT" % delta)
        
        #time.sleep(0.1)


if __name__ == '__main__':
    try:
        BLE.init_ble()
        BLE.advertise()
        field_watch('police')



    except (KeyboardInterrupt, SystemExit) as exErr:
        lcd.setFastBacklight(0, 0, 0)
        lcd.clearScreen()
        pump.disable()
        buzzer.off()
        
        print('problem')
        sys.exit(0)
