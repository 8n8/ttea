import time
import serial
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def do_experiment():
    com = 'COM4'
    ser = serial.Serial(
        port = com,
        baudrate=250000,
        )

do_experiment()
    
