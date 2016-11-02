import time
import serial
import os, sys
import numpy as np
import matplotlib.pyplot as plt

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

f = open('temperatures.txt', 'w') ## opens text file to print recordings to
print(f)
m = 0
nozzle_data = np.array([0])         ## Creates a numpy array to store the nozzel temperature to
## bed_data = np.array([0])         ##Uncomment for bed data
t = np.array([0])                   ## Creates a numpty array to store times to
timestep = 0.5
max = 420

time.sleep(1)                       ## Sleep for 1 second
ser.setDTR(0)                       ##This is needed to reset the printer before writing
time.sleep(1)

ser.write(b'M42 P9 S255\r\n')       ## Write G-code over serial command, turns on RAMPS fan
ser.write(b'M42 P4 S255\r\n')       ## turns on horizontal extruder fan
ser.write(b'M106 S200\r\n')         ## turns on small nozzle fan

# User inputs the required PID values
print('Enter value for K_p:')
K_p = input(">>")
print('Enter value for K_i:')
K_i = input(">>")
print('Enter value for K_d:')
K_d = input(">>")

ser.write(b'M301 P' + K_p.encode() + b' I' + K_i.encode() + b' D' + K_d.encode() + b'\r\n') ## Sets PID parameters
time.sleep(2) ##giving the printer a chance to respond before reading...
print('Wait for three minutes!')
print(ser.readline)

ser.write(b'M104 S100\r\n')         ##Sets the nozzle target temperature to 100 degrees
##ser.write(b'M140 S50\r\n')        ##Uncomment for bed data; sets the bed target temperature to 50 degrees

for m in range(1,max):              ## For loop to read obtaining temperature values for max time limit
    ser.write(b'M105\r\n')         
    out = ''
    ## waits amount set by timestep before reading output
    time.sleep(timestep)
    out = ser.read(ser.inWaiting()) ## Wait for serial data incoming from 3D printer
    s = str(out)
    if out != '' and ':' in s and 'S' not in s:         ## makes sure only to use temperature reading lines
        colon = s.find(':')                             ## finds the first colon in string
        nozzle_temp = s[(colon + 1):(colon + 6)]        ## nozzle temp in this range after first colon
        ##s = s[(colon + 6):] ## strips away nozzle temp colon, uncomment for bed data
        ##colon = s.find(':') ## finds the new first colon, uncomment for bed data
        ##bed_temp = s[(colon + 1):(colon + 6)] ##uncomment for bed data, bed temp should now be in this range after the new colon
        nozzle_data = np.append(nozzle_data, [nozzle_temp])
        ##bed_data = np.append(bed_data, [bed_temp])##uncomment if recording bed data
        tim = str(m*timestep)
        t = np.append(t, [tim])
        ##f.write(tim + ' ' + nozzle_temp + ' ' + bed_temp + '\r\n')##uncomment this if recording bed and nozzle
        f.write(tim + ' ' + nozzle_temp + '\r\n')       ##comment this out if recording bed data

f.close()
ser.write(b'M104 S0\r\n')               ## turns off nozzle heater
time.sleep(1)
ser.write(b'M106 S255\r\n')             #Start cooling down the nozzel for future PID tests
##ser.write(b'M140 S0\r\n') ##UNCOMMENT THIS FOR BED DATA; turns off bed heater

plt.figure(1)                           ## Create Figure
plt.plot(t, nozzle_data, 'r-')          ## Plot time agains nozzel temperature (np arrays)
plt.ylabel('Nozzle Temperature')
plt.xlabel('Time')

##plt.figure(2)
##plt.plot(t, bed_data, 'k')
##plt.ylabel('Bed Temperature') 
##plt.xlabel('Time')##Uncomment this block for bed data graph

print('Please enter a filename for the nozzle graph and the data (.txt) document (no punctuation except \'-\' and \'_\'):')
figname= input(">>")

plt.figure(1).savefig(figname + '.pdf', bbox_inches='tight')

##print('Please enter a filename for the bed graph and the data (.txt) document (no punctuation except \'-\' and \'_\'):')
##figname= input(">>") 
##plt.figure(2).show()
##plt.figure(2).savefig(figname + '.pdf', bbox_inches='tight') ##Uncomment this block for bed data

plt.figure(1).show()

os.rename('temperatures.txt', figname + '.txt')

ser.close()
print('done')


