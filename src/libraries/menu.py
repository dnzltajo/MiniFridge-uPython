import time
from machine import I2C, Pin
from rotary_irq_esp import RotaryIRQ
from esp8266_i2c_lcd import I2cLcd

i2c=I2C(scl=Pin(5),sda=Pin(4))
lcd=I2cLcd(i2c,0x27,2,16)
sw = Pin(2,Pin.IN,Pin.PULL_UP)
#functions
def set_htime():
  r = RotaryIRQ(pin_num_clk=14, pin_num_dt=13, min_val=0, max_val=23, reverse=True, range_mode=RotaryIRQ.RANGE_BOUNDED)
  lastval = r.value()
  while True:
    val = r.value() 
    if lastval != val:
      lastval = val
      lcd.move_to(0,1)
      lcd.putstr("")
      lcd.putchar(chr(62))
      if val<10:
        lcd.putstr("        0%d:00 " %val)
      else:
        lcd.putstr("        %d:00 " %val)
    if sw.value()==0:
      x=val
      return x

def set_mtime(check,max,x):
  if check==x: 
    r = RotaryIRQ(pin_num_clk=14, pin_num_dt=13, min_val=0, max_val=max, reverse=True, range_mode=RotaryIRQ.RANGE_BOUNDED)
  elif (check+1)==x: 
    r = RotaryIRQ(pin_num_clk=14, pin_num_dt=13, min_val=max, max_val=59, reverse=True, range_mode=RotaryIRQ.RANGE_BOUNDED)
  else:
    r = RotaryIRQ(pin_num_clk=14, pin_num_dt=13, min_val=0, max_val=59, reverse=True, range_mode=RotaryIRQ.RANGE_BOUNDED)
  lastval = r.value()
  while True:
    val = r.value() 
    if lastval != val:
      lastval = val
      lcd.move_to(0,1)
      lcd.putstr("")
      lcd.putchar(chr(62))
      if x<10 and val<10:
        lcd.putstr("        0%d:0%d " %(x,val))
      elif x<10 and val>9:
        lcd.putstr("        0%d:%d " %(x,val))   
      elif x>9 and val<10:
        lcd.putstr("        %d:0%d " %(x,val))           
      else:
        lcd.putstr("        %d:%d " %(x,val)) 
    if sw.value()==0:
      return val

def time_menu():
  while True:
    #Start Time
    lcd.clear()
    lcd.putstr("Start Time:\n")
    w=set_htime()
    time.sleep_ms(500)
    x=set_mtime(0,0,w)
    time.sleep_ms(500)
    lcd.clear()
    #End Time
    lcd.putstr("End Time:\n")
    y=set_htime()
    time.sleep_ms(500)
    z=set_mtime(w,x,y)
    time.sleep_ms(500)
    lcd.clear()
    #START TIME DISPLAY
    if w<10 and x<10:
      lcd.putstr("Start: 0%d:0%d\n" %(w,x))
    elif w<10 and x>9:
      lcd.putstr("Start: 0%d:%d\n" %(w,x))   
    elif w>9 and x<10:
      lcd.putstr("Start: %d:0%d\n" %(w,x))           
    else:
      lcd.putstr("Start: %d:%d\n" %(w,x))
    #END TIME DISPLAY
    if y<10 and z<10:
      lcd.putstr("End: 0%d:0%d" %(y,z))
    elif y<10 and z>9:
      lcd.putstr("End: 0%d:%d" %(y,z))   
    elif y>9 and z<10:
      lcd.putstr("End: %d:0%d" %(y,z))           
    else:
      lcd.putstr("End: %d:%d" %(y,z))     
    time.sleep_ms(5000)
    lcd.clear()
    return w, x, y, z

def temp_menu():
  r = RotaryIRQ(pin_num_clk=14, pin_num_dt=13, min_val=9, max_val=30, reverse=True, range_mode=RotaryIRQ.RANGE_BOUNDED)
  lastval = r.value()
  lcd.clear()
  lcd.putstr("Temperature:\n")
  while True:
    val = r.value() 
    if lastval != val:
      lastval = val
      lcd.move_to(0,1)
      lcd.putstr("")
      lcd.putchar(chr(62))
      if val == 9:
        lcd.putstr("         OFF")
      else: 
        lcd.putstr("        %d" %val)
        lcd.putchar(chr(223))
        lcd.putstr("C")
    if sw.value()==0:
      lcd.clear()
      if val == 9:
        lcd.putstr("Temp:  OFF")
      else: 
        lcd.putstr("Temp: %d"%val)
        lcd.putchar(chr(223))
        lcd.putstr("C")
      time.sleep_ms(5000)
      return val
 

















