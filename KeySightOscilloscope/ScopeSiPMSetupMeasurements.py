import os
import serial   
import numpy as np
import matplotlib.pyplot as plt
# Import necessary packages
import pyvisa as visa
import pandas as pd
from time import sleep

import keyoscacquire.oscacq as koa

def averaged_trace(scope, measurement_number, averages=1):
    # Set the number of averages and get a trace
    # Save the trace data as a csv and a png plot, without showing the plot
    # (the averaging mode and the number of averages is also automatically
    # saved inside the file, together with a timestamp and more)
    scope.set_options_getTrace_save(fname=f"../FirstSLArPAAS_SiPMChannel_ColdTest/roomtemp_68p2mVtrigger_2pf_2p7kohm_OnlyPreAmpNoBias_{measurement_number}",num_points=1000)

def different_averaging():
    # Connect to the scope
    scope = koa.Oscilloscope(address='USB0::10893::6006::MY58262555::0::INSTR')
        # Set the channels to view on the scope
    scope.active_channels = [1]
    # Prepare a two panel plot
   
    # Obtain traces for different numbers of averages
    for i in range(500):
        averaged_trace(scope, i)
        # Plot channel 1 to ax[0] and ch 3 to ax[1]

different_averaging()

