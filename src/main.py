#--------------------------------
# Programmable Mini Refrigerator
#           DB.Tajo
#          2019-2020
#--------------------------------

import gc
gc.collect()
import time
gc.collect()
import onewire, ds18x20
gc.collect()
from machine import I2C, Pin
gc.collect()
from esp8266_i2c_lcd import I2cLcd
gc.collect()
import ds1307
gc.collect()
import menu
gc.enable()

#setup
sw = Pin(2,Pin.IN,Pin.PULL_UP)
pb2 = Pin(0,Pin.IN,Pin.PULL_UP)
relay = Pin(12,Pin.OUT)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(Pin(3)))
roms = ds_sensor.scan()
i2c=I2C(scl=Pin(5),sda=Pin(4))
lcd=I2cLcd(i2c,0x27,2,16)
ds= ds1307.DS1307(i2c)
lcd.backlight_on()
lcd.clear()
lcd.putstr("  Programmable\n Mini    Fridge")
time.sleep_ms(3000)
lcd.clear()
gc.collect()
 
#Main Loop
while True:
  clock = ds.datetime()
  gc.collect()
  lcd.move_to(0, 0)
  lcd.putstr("Time: ")
  lcd.putstr("%d:" %(clock[4]))
  if clock[5]<10:
    lcd.putstr("0%d:" %(clock[5]))
  else:
    lcd.putstr("%d:" %(clock[5]))
  lcd.putstr("%d " %(clock[6]))
  ds_sensor.convert_temp()
  for rom in roms:
    temp=ds_sensor.read_temp(rom)
  lcd.putstr("\nTemp: %.2f"%(temp))
  lcd.putchar(chr(223))
  lcd.putstr("C")
  gc.collect()  
  f=open('time.txt')
  tmset=f.read()
  tlist=tmset.split(",")
  shr=int(tlist[0])
  smin=int(tlist[1])
  ehr=int(tlist[2])  
  emin=int(tlist[3])
  f.close()
  xhr=int(clock[4])
  xmin=int(clock[5])
  gc.collect()
  f=open('temp.txt')
  tpset=f.read()
  xtmp=int(tpset)
  f.close()
  gc.collect()
 
  if shr<ehr:  # 0 -> 24
    if (shr==xhr and smin==xmin) or (shr==xhr and smin<xmin): 
      if  temp > (xtmp + 2):
        relay.value(1)
      elif temp < xtmp:
        relay.value(0)    
    elif (shr<xhr and xhr<ehr):
      if  temp > (xtmp + 2):
        relay.value(1)
      elif temp < xtmp:
        relay.value(0)   
    elif (ehr==xhr and emin==xmin) or (ehr==xhr and xmin<emin):
      if  temp > (xtmp + 2):
        relay.value(1)
      elif temp < xtmp:
        relay.value(0)           
    else:
      relay.value(0) 
 

  if shr>ehr or shr==ehr: #24 -> 0
    if (shr==xhr and smin==xmin) or (shr==xhr and smin<xmin): 
      if  temp > (xtmp + 2):
        relay.value(1)
      elif temp < xtmp:
        relay.value(0)
    elif (shr<xhr or ehr>xhr):
      if  temp > (xtmp + 2):
        relay.value(1)
      elif temp < xtmp:
        relay.value(0)  
    elif (ehr==xhr and emin==xmin) or (ehr==xhr and emin>xmin):
      if  temp > (xtmp + 2):
        relay.value(1)
      elif temp < xtmp:
        relay.value(0)      
    elif (shr==ehr and smin==emin):
      if  temp > (xtmp + 2):
        relay.value(1)
      elif temp < xtmp:
        relay.value(0)  
    else:
      relay.value(0)
  
  gc.collect()
  if sw.value()==0:  #Change Time and Temp Settings 
    time.sleep_ms(500)
    if sw.value()==0:
      lcd.clear()
      time.sleep_ms(500)
      start_hr,start_min,end_hr,end_min = menu.time_menu()
      f=open('time.txt','w')
      f.write('%d,%d,%d,%d'%(start_hr,start_min,end_hr,end_min))
      f.close()
      gc.collect()
    else:
      lcd.clear()
      time.sleep_ms(500)
      temp=menu.temp_menu()    
      f=open('temp.txt','w')
      f.write('%d' %temp)
      f.close()
      gc.collect()
  elif pb2.value()==0: #Dispay Current Settings YELLOW
    lcd.clear()
    if shr<10 and smin<10:
      lcd.putstr("Time~0%d:0%d" %(shr,smin))
    elif shr<10 and smin>9:
      lcd.putstr("Time~0%d:%d" %(shr,smin))   
    elif shr>9 and smin<10:
      lcd.putstr("Time~%d:0%d" %(shr,smin))           
    else:
      lcd.putstr("Time~%d:%d" %(shr,smin))
    #END TIME DISPLAY
    if ehr<10 and emin<10:
      lcd.putstr("-0%d:0%d" %(ehr,emin))
    elif ehr<10 and emin>9:
      lcd.putstr("-0%d:%d" %(ehr,emin))   
    elif ehr>9 and emin<10:
      lcd.putstr("-%d:0%d" %(ehr,emin))           
    else:
      lcd.putstr("-%d:%d" %(ehr,emin))      
    lcd.putstr("Temp~ %d" %xtmp)
    lcd.putchar(chr(223))
    lcd.putstr("C")
    time.sleep_ms(3500)
    lcd.clear()
