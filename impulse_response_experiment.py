"""
This program runs an experiment on a 3D printer and
captures the impulse response of the nozzle.  This 
file is structured as several small functions that 
are used in the do_it_all function at the bottom of the
file.
"""

import serial
import time
import csv
import matplotlib.pyplot as plt


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
    return(r != '' and ':' in r and 'S' not in r)


def extract_temp_from_reading(reading):
    """ 
    It extracts the temperature from the data produced
    by the printer.
    """
    colon = reading.find(':')
    return(reading[(colon+1):(colon+6)])


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
    ser = serial.Serial(port='COM4',baudrate=250000)
    
    time.sleep(1)
    ser.setDTR(0)
    time.sleep(1)

    kp = 1
    ki = 0
    kd = 0

    ser.write(b'M301 P' + kp.encode() + b' I' +
              ki.encode() + b' D' + kd.encode()
              + b'\r\n') 

    time.sleep(2)
    return(ser)


def impulse(ser):
    """ It sends an impulse to the printer. """
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
    data = take_n_readings(400)
    write_data_to_file(data,'impulse_response.csv')
    plot_data(data)

    
do_it_all()    
    




