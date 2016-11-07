import serial

def do_experiment():
    print('COM PORT PLEASE :)')
    com = input(">>")
    ser = serial.Serial(
        port = com,
        baudrate=250000,
        )
    

do_experiment()
    
