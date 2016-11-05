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
