"""
Copyright 2016 True Ghiassi <true@ghiassitrio.co.uk>

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

*Description*

The code in this file runs an experiment to try to find the 
best PID parameters for the controller of the printer.
"""

#import serial
import impulse_response_experiment as ire
from scipy.optimize import minimize


def setup_link():
    ser = serial.Serial(port='COM4',baudrate=250000)

    time.sleep(1)
    ser.setDTR(0)
    time.sleep(1)

    return ser


def set_pid(ser,k):
    skp = str(k[0])
    ski = str(k[1])
    skd = str(k[2])
    ser.write(b'M301 P' + skp.encode() + b' I' +
              ski.encode() + b' D' + skd.encode()
              + b'\r\n')
    time.sleep(1)
    

def wait_till_95_deg(ser):
    """ 
    It sets the temperature to 95 degrees and waits till it
    gets there.
    """
    print('Waiting till 95 degrees ...')
    ser.write(b'M104 S95\r\n')
    temp = float(ire.one_reading(ser))
    while temp < 94.5 or temp > 95.5:
        if temp > 95.5:
            ser.write(b'M106 S255\r\n')
        else:
            ser.write(b'M106 S0\r\n')
        temp = float(ire.one_reading(ser))
    print('reached 95 degrees')
    return


def take_readings(ser):
    """ It takes 120 readings. """ 
    start = time.time()
    raw_results = [[time.time()-start, ire.one_reading(ser)]
                   for i in range(120)]
    return [x for x in raw_results if x[1] != None]
    

def one_test(ser,k):
    wait_till_95_deg(ser)
    set_pid(ser,k)
    return take_readings(ser)


def quality(data):
    q =  max([float(x[0]) for x in data
              if float(x[1]) < 99 or float(x[1]) > 101])
    print('quality: '+str(q))
    return q


def optimise():
    ser = setup_link()
    testno = 0
    def test(k):
        if min(k) < 0: return 1000
        data = one_test(ser,k)
        ire.write_data_to_file(data,'pid_'+str(testno)+'_'+
                               '_'+str(k[0])+'_'+
                               str(k[1])+'_'+str(k[2])+'.csv')
        testno += 1
        return -quality(data)
    k0 = [20.5,0.515,204]
    bnds = ([5,0,50],[100,20,400])
    res = minimize(test,k0,method='BFGS',
                   options={'maxiter':60,'disp':True})
    best_test = one_test(ser,res.x)
    ser.close()
    ire.plot_data(best_test)
    return res.x


#optimise()
    
    
    
    


    
    
    

    

