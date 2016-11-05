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
"""


"""
A few simple tests for the functions in 
impulse_response_experiment that are easy to test.
When run, this script should print out True, True ... etc.
If there is a False then a test has failed.
"""

import impulse_response_experiment as ire

def test_valid_reading():
    inputs = ['','abc:2','a:sdfSs']
    expected_output = [False,True,False]
    output = [ire.valid_reading(x) for x in inputs]
    if output != expected_output: return False
    return True

print(test_valid_reading())

def test_extract_temp_from_reading():
    input = 'asdf:123.4534asdf'
    expected_output = '123.4'
    output = ire.extract_temp_from_reading(input)
    if output != expected_output: return False
    return True

print(test_extract_temp_from_reading())
