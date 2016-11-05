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


def data_set(data,a,b,c):
    """ 
    a,b, and c are the parameters for the theoretical 
    impulse response and data is the experimental data 
    set.  This function will calculate the theoretical 
    data set.
    """
    t = [i[0] for i in data]
    return [impulse_response(tt,a,b,c) for tt in t]


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
    a_range = np.linspace(0,10,20)
    b_range = np.linspace(0,10,20)
    c_range = np.linspace(0,10,20)
    y_vals = [d[1] for d in data]
    return ({'gap':data_diff(data_set(data,a,b,c), y_vals),
             'a':a, 'b':b, 'c':c}
            for a in a_range
            for b in b_range
            for c in c_range)


def convert_2_float(data):
    return [[float(x[0]),float(x[1])] for x in data]


def optimise():
    """
    It finds the set of parameters that give the smallest
    least-squares difference with the experimental data set.
    """
    data = convert_2_float(
        read_data_from_file('impulse_response.csv'))
    return min(all_data_sets(data), key=lambda x:x['gap'])


print(optimise())


