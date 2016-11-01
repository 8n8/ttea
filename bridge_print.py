import time
import serial
import numpy as np
import matplotlib.pyplot as plt

bar_height = 51       ## Sets the height of the bars used in to create the strings                       

print('please input the name of the port that the printer is connected to (e.g. COM6)')
com = input(">>")

if 'ser' in globals() and ser.isOpen() == False: ## checks if ser is defined already and if connection is open
    ## configures the serial connection:
    ser = serial.Serial(
        port = com,
        baudrate=250000,
    )
elif 'ser' in globals() and ser.isOpen() == True:
    ser.flushInput()
    ser.flushOutput()
else:
    ser = serial.Serial(
        port = com,
        baudrate=250000,
    )
time.sleep(1)
ser.setDTR(0)                       ##This is needed to reset the printer before writing
time.sleep(1)

ser.write(b'M42 P9 S255\r\n')       ## turns on RAMPS fan
ser.write(b'M42 P4 S255\r\n')       ## turns on horizontal extruder fan
ser.write(b'M106 S100\r\n')         ## turns on small nozzle fan

ser.write(b'M140 S70\r\n')          ##heats bed to 70C
ser.write(b'M104 S210\r\n')         ##heats nozzle to 210C


##make sure the printer is at these coords before starting, or alter this command so the coordinates are correct.
ser.write(b'G92 X100 Y0 Z70\r\n')   ##calibrates printer so it shows the correct position
ser.write(b'G1 F200 E5\r\n')        ## extrude 3mm of feed stock to check working
ser.write(b'G92 E0\r\n')            ##resets extrusion amount to zero

height = str(bar_height)            ##height of platforms
print('Are the bed and nozzle up to temperature? (see LCD screen on printer)')
i = input(">>")
ser.write(b'G0 F120 Z' + height.encode() + b'\r\n')
m = 0

for n in range(0,13):               ## For loop to repeat printing 13 strings

    y_pos = 5 + n*15                ## Updates y position each iteration of the loop
    y_pos = str(y_pos)              ## Converts y_pos integer to string
        
    ext_amt = 1 + m
    ext_amt = str(ext_amt)
    print(ext_amt)
    
    feed = 3000                     ## setting a desired feedrate, 
    feed = str(feed)                ## Convert integer to string
    print(feed)

    if (n+3) % 2 == 0:              ##only increases setting after every even thread printed
        m = m + 1
        
    ser.write(b'G92 E0\r\n')        ##resets extrusion amount to zero

    ser.write(b'G1 F' + feed.encode() + b'\r\n')
    ser.write(b'G0 F' + feed.encode() + b' X53 Y' + y_pos.encode() + b'\r\n') ##Moves in postion for extrudes
    height = str(bar_height)
    ser.write(b'G0 F120 Z' + height.encode() + b'\r\n') ## Set Z position to bar height
    ser.write(b'G1 F900 E12\r\n')                       ## Extrude feed stock (starting blob)
    ser.write(b'G92 E0\r\n')                            ## Resets extrusion amount to zero
    ser.write(b'G1 F' + feed.encode() + b'\r\n')        ## Set feed rate

    ser.write(b'G1 F' + feed.encode() + b' X153 E' + ext_amt.encode() + b'\r\n') ##moves to next web point
    ser.write(b'G92 E0\r\n')                            ##resets extrusion amount to zero
    ser.write(b'G1 F900 E12\r\n')                       ## Extrude feed stock (end blob)

    print('Has this line finished?')                    ##necessary to send the code in blocks
    i = input(">>")

    height = str(bar_height+2)
    ser.write(b'G0 F120 Z' + height.encode() + b'\r\n') ##Raise Z Axis slighly

print("Send final 'home' command")
i = input(">>")
ser.write(b'G0 F9000 X100 Y0 Z70\r\n')                  ## Return the print head to the 'home' position
print("Finished...")
ser.write(b'M104 S0\r\n')                               ##turns off heater
ser.write(b'M42 P4 S0\r\n')                             ## turns on horizontal extruder fan
ser.write(b'M106 S0\r\n')                               ## turns on small nozzle fan

ser.close()
