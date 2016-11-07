"""
Copyright 2016 True Ghiassi <true@ghiassitrio.co.uk>
and Tinaes <ta371@cam.ac.uk>

This file is part of TTea.   

TTea is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TTea is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TTea.  If not, see <http://www.gnu.org/licenses/>.
"""

import serial
import time
import csv
import matplotlib.pyplot as plt

"""
This program runs an experiment on a 3D printer and
captures the impulse response of the nozzle.  This 
file is structured as several small functions that 
are used in the do_it_all function at the bottom of the
file.
"""


def get_data_from_printer(ser):
    """ 
    It waits for a short time and takes a temperature 
    reading.
    """
    ser.write(b'M105\r\n')
    time.sleep(0.5)
    return(ser.read(ser.inWaiting()))


def valid_reading(r):
    """ 
    It checks if the data from the printer contains 
    the needed information.
    """
    s = str(r)
    return(r != '' and ':' in s and 'S' not in s)


def extract_temp_from_reading(reading):
    """ 
    It extracts the temperature from the data produced
    by the printer.
    """
    s = str(reading)
    colon = s.find(':')
    return(s[(colon+1):(colon+6)])


def one_reading(ser):
    """
    It asks the printer for a reading, checks it is 
    valid, and extracts the temperature from the 
    reading.
    """
    dat = get_data_from_printer(ser)
    if not valid_reading(dat): return
    temperature = extract_temp_from_reading(dat)
    return(temperature)


def setup_link():
    """ It will connect to the printer. """
    print('Connecting to Printer...')
    ser = serial.Serial(port='COM4',baudrate=250000)
    
    time.sleep(1)
    ser.setDTR(0)
    time.sleep(1)

    kp = '1.0'
    ki = '0.0'
    kd = '0.0'

    ser.write(b'M301 P' + kp.encode() + b' I' +
              ki.encode() + b' D' + kd.encode()
              + b'\r\n')
    print('PID Values set to 1,0,0')

    time.sleep(2)
    return(ser)


def impulse(ser):
    """ It sends an impulse to the printer. """
    print('Sending Impulse')
    ser.write(b'M104 S999\r\n')
    time.sleep(2)
    ser.write(b'M104 S0\r\n')


def take_n_readings(n):
    """
    It will run an experiment on the printer to find
    the impulse response.
    """
    ser = setup_link()

    impulse(ser)

    start = time.time()

    raw_results = [[time.time()-start,one_reading(ser)] for i in range(n)]
    results_with_no_nulls = [x for x in raw_results if x[1] != None] 
    return(results_with_no_nulls)


def write_data_to_file(data,filename):
    """
    The data is a list of lists, with each inner list being a time
    and a temperature.
    """
    with open(filename,'w') as f:
        csv.writer(f).writerows(data)
    
        
def plot_data(data):
    print('Plotting...')
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    plt.plot(x,y,'r-')
    plt.ylabel('Nozzle temperature')
    plt.xlabel('Time')
    plt.savefig('impulse_response.eps',format='eps',dpi=1000)
        

def do_it_all():
    """
    It uses the functions defined above to run the experiment,
    save the data to a file and plot it.
    """
    data = take_n_readings(40)
    write_data_to_file(data,'impulse_response.csv')
    print('Data written to impulse_response.csv')
    plot_data(data)

    
do_it_all()    
    




