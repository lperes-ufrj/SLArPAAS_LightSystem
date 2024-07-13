import os
import serial   
import numpy as np
import matplotlib.pyplot as plt
# Import necessary packages
from pymeasure.instruments.keithley import Keithley2450
import pyvisa as visa
import pandas as pd
from time import sleep

import keyoscacquire.oscacq as koa


def get_averaged(osc_address, averages=1):
    scope = koa.Oscilloscope(address=osc_address)
    time, volts, channels = scope.set_options_getTrace(acq_type='AVER'+str(averages))
    scope.close()
    return time, volts, channels


time, volts, channels = get_averaged('USB0::10893::6006::MY58262555::0::INSTR')
for y, ch in zip(volts.T, channels): # need to transpose volts: each row is one channel
    plt.plot(time, y, label=ch)
    plt.legend()
    plt.show()