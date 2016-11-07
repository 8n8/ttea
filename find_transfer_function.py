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

*Program description*

It find the parameters for a transfer function given the 
experimental impulse response data for a system.
"""

import csv
import math
import matplotlib.pyplot as plt
import numpy as np


def read_data_from_file(filename):
    with open(filename,'r') as f:
        return list(csv.reader(f))


def impulse_response(t,a,b,c):
    """
    This is the theoretical impulse response.  It is 
    assumed to be a decaying exponential with a time
    delay.  
    """
    return a*math.exp(-b*(t-c))


def data_set(times,a,b,c):
    """ 
    a,b, and c are the parameters for the theoretical 
    impulse response and data is the experimental data 
    set.  This function will calculate the theoretical 
    data set.
    """
    return [impulse_response(t,a,b,c) for t in times]


def data_diff(dat1,dat2):
    """
    It will do a least_squares comparison between two
    lists of data.
    """
    return sum((d1-d2)**2 for d1,d2 in zip(dat1,dat2))


def all_data_sets(data):
    """
    It makes all the possible data sets.
    """
    a_range = np.linspace(0,10,10)
    b_range = np.linspace(0,10,60)
    c_range = np.linspace(0,10,60)
    y_vals = [d[1] for d in data]
    times = [d[0] for d in data]
    return ({'gap':data_diff(data_set(times,a,b,c), y_vals),
             'a':a, 'b':b, 'c':c}
            for a in a_range
            for b in b_range
            for c in c_range)


def convert_2_float(data):
    return [[float(x[0]),float(x[1])] for x in data]


def optimise(data):
    """
    It finds the set of parameters that give the smallest
    least-squares difference with the experimental data set.
    """
    return min(all_data_sets(data), key=lambda x:x['gap'])


def plot_data(data,p):
    """ 
    p is a dictionary containing the impulse response
    parameters.
    """
    x = [i[0] for i in data]
    y1 = [i[1] for i in data]
    plt.plot(x,y1,'r-',label='data')
    y2 = data_set(x,p['a'],p['b'],p['c'])
    plt.plot(x,y2,'g-',label='model')
    plt.ylabel('Nozzle temperature')
    plt.xlabel('Time')
    plt.legend(loc='upper right')
    plt.savefig('impulse_response.eps',format='eps',dpi=1000)
    plt.show()

def do_it_all():
    data = convert_2_float(
        read_data_from_file('small_impulse_response.csv'))
    p = optimise(data)
    plot_data(data,p)

do_it_all()


