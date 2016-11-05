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
