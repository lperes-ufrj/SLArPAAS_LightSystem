## Simplest Code possible for the SiPMs, Drops the Bias voltage for -60V and measures the current.

import os
import serial   
import numpy as np
import matplotlib.pyplot as plt
# Import necessary packages
from pymeasure.instruments.keithley import Keithley2450
import pyvisa
import pandas as pd
from time import sleep


data_points = 50 


from pymeasure.adapters import VISAAdapter

adapter = VISAAdapter("USB0::0x05e6::0x2450::04614968::INSTR")
keithley = Keithley2450(adapter)

keithley.apply_voltage()                # Sets up to source voltage
keithley.source_voltage_range = -60  # Sets the source voltage range to -55 V
keithley.compliance_current = 1e-4        # Sets the compliance current to 100 mu A.
keithley.source_voltage = 0             # Sets the source voltage to 0 Volts.
keithley.enable_source()                # Enables the source output
keithley.measure_current()              # Sets up to measure voltage


# Allocate arrays to store the measurement results
voltage_probe = np.linspace(-52,-60,data_points)
currents = np.zeros_like(voltage_probe)
currents_stds = np.zeros_like(currents)

for i in range(data_points):

    keithley.ramp_to_voltage(voltage_probe[i])  # Ramps the current to 5 mA
    sleep(.5)
    currents[i] = keithley.current  # Save current
    currents_stds[i] = keithley.std_current # Save current std
    sleep(.5)

# Save the data columns in a CSV file
data = pd.DataFrame({
    'Current (A)': currents,
    'Voltage (V)': voltages,
    'Current Std (A)': currents_stds,
})
data.to_csv('IV_Curve.csv')


keithley.shutdown()                     # Ramps the current to 0 mA and disables output