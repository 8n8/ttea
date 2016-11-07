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

It uses a model of the system's impulse response to find the 
optimum PID parameters for the controller.
"""

import math


def system_transfer_function(s,p,i,d,a=6,b=15,c=5):
    """
    The system is a PID controller in series with
    a system whose impulse response is a time-delayed
    decaying exponential.
    """
    return (p + (i/s) + d*s) * (a*math.exp(c) / (s+b))

    
def input_signal(omega,amplitude):
    return amplitude * math.sin(omega*t) 





