## Simplest Code possible for the SiPMs, Drops the Bias voltage for -60V and measures the current.

import os
import sys
import usb.core
import serial   
import numpy as np
import matplotlib.pyplot as plt
# Import necessary packages
from pymeasure.instruments.keithley import Keithley2450
import pyvisa
import pandas as pd
from time import sleep
import time


data_points = 100


from pymeasure.adapters import VISAAdapter


dev = usb.core.find(idVendor=0x05e6,idProduct=0x2450)
ep = dev[0].interfaces()[0].endpoints()[0]
i = dev[0].interfaces()[0].bInterfaceNumber

dev.reset()



if dev.is_kernel_driver_active(i):
    try:
        dev.detach_kernel_driver(i)
    except usb.core.USBError as e:
        sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))



adapter = VISAAdapter("USB0::0x05e6::0x2450::04614968::INSTR")
keithley = Keithley2450(adapter)

keithley.reset()
keithley.apply_voltage()                # Sets up to source voltage
keithley.source_voltage_range = -60  # Sets the source voltage range to -55 V
keithley.compliance_current = 1e-4        # Sets the compliance current to 100 mu A.
keithley.source_voltage = -60             # Sets the source voltage to 0 Volts.
keithley.enable_source()                # Enables the source output
keithley.measure_current()              # Sets up to measure voltage


# Allocate arrays to store the measurement results
voltage_probe = np.linspace(-60,-50,data_points)
currents = np.zeros_like(voltage_probe)
currents_stds = np.zeros_like(voltage_probe)
#print(currents)
#print(currents_stds)

for i in range(data_points):
    
    keithley.source_voltage = voltage_probe[i]# Ramps the current to 5 mA
    currents[i] = keithley.current  # Save current
    sleep(.2)
    #currents_stds[i] = keithley.std_current # Save current std

# Save the data columns in a CSV file
data = pd.DataFrame({
    'Voltage (V)': voltage_probe,
    'Current (A)': currents,
    #'Current Std (A)': currents_stds,
})
keithley.source_voltage = 0 
keithley.reset() 
keithley.shutdown()      

filename = 'SiPM_IV_Curve'+str(time.strftime("%Y%m%d%M"))+'.csv'
data.to_csv(filename)

data = pd.read_csv(filename,usecols=['Voltage (V)','Current (A)']) 
# Read the CSV file into a pandas DataFrame

data.head()

# Extract the columns
voltage_plot = data.iloc[:, 0] 
current_plot = data.iloc[:, 1]*10**6
#current_std_plot = data.iloc[:, 2]*10**6

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(-voltage_plot, current_plot, marker='.', linestyle='--')
plt.ylabel(r'Current ($\mu$A)')
plt.xlabel('Reverse Voltage (V)')
plt.title('Plot of CSV Data Oscilloscope')
plt.grid()

plt.show()

