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

The code in this file runs some simple tests on pid_experiment.py.
"""

import pid_experiment as pex
from scipy.optimize import minimize

def test_quality():
    inp = [['1','102'],['2','100'],['3.1','98.5'],['4','100']]
    ex_output = 3.1 
    return pex.quality(inp) == ex_output

print(test_quality())

def x_squared(x):
    return x[0]**2+x[1]**(0.5)
bnds = ([0,0],[50,50])

print(minimize(x_squared,[5,2],method='BFGS',options={'maxiter':600,'bounds':bnds,'disp':True}))

    
